from flask import Blueprint, jsonify, request
from flask_login import current_user
from models import Post, User, Comment, Tag, db
from functools import wraps
import jwt
from datetime import datetime, timedelta
from config import Config

api_bp = Blueprint('api', __name__, url_prefix='/api')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@api_bp.route('/token', methods=['POST'])
def get_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify'}), 401
    
    user = User.query.filter_by(email=auth.username).first()
    if not user or not user.check_password(auth.password):
        return jsonify({'message': 'Could not verify'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, Config.SECRET_KEY)
    
    return jsonify({'token': token})

@api_bp.route('/posts')
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc())
    pagination = posts.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'posts': [{
            'id': post.id,
            'title': post.title,
            'excerpt': post.excerpt,
            'author': post.author.username,
            'created_at': post.created_at.isoformat(),
            'tags': [tag.name for tag in post.tags]
        } for post in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@api_bp.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    if not post.is_published:
        return jsonify({'message': 'Post not found'}), 404
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': {
            'username': post.author.username,
            'bio': post.author.bio
        },
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'tags': [tag.name for tag in post.tags],
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'created_at': comment.created_at.isoformat()
        } for comment in post.comments.filter_by(is_approved=True)]
    })

@api_bp.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    post = Post(
        title=data['title'],
        content=data['content'],
        excerpt=data.get('excerpt'),
        is_published=data.get('is_published', False),
        author=current_user
    )
    
    # Handle tags
    if 'tags' in data:
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            post.tags.append(tag)
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({
        'message': 'Post created successfully',
        'post_id': post.id
    }), 201

@api_bp.route('/posts/<int:id>', methods=['PUT'])
@token_required
def update_post(current_user, id):
    post = Post.query.get_or_404(id)
    
    if post.author != current_user:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'excerpt' in data:
        post.excerpt = data['excerpt']
    if 'is_published' in data:
        post.is_published = data['is_published']
    
    # Update tags
    if 'tags' in data:
        post.tags.clear()
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            post.tags.append(tag)
    
    db.session.commit()
    
    return jsonify({'message': 'Post updated successfully'})

@api_bp.route('/posts/<int:id>', methods=['DELETE'])
@token_required
def delete_post(current_user, id):
    post = Post.query.get_or_404(id)
    
    if post.author != current_user and not current_user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted successfully'})

@api_bp.route('/posts/<int:id>/comments', methods=['POST'])
@token_required
def create_comment(current_user, id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    comment = Comment(
        content=data['content'],
        author=current_user,
        post=post,
        is_approved=True if current_user.is_admin else False
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'message': 'Comment created successfully',
        'comment_id': comment.id
    }), 201

    