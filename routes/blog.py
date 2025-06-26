from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import Post, Comment, Tag, Reaction, db, Follow, UserTagFollow, CommentUpvote, Badge, UserBadge, User
from forms.blog import PostForm, CommentForm
from markdown import markdown
from sqlalchemy import or_

from sqlalchemy import desc, func
blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    # If user is logged in and wants personalized feed
    if current_user.is_authenticated and request.args.get('feed') == 'following':
        followed_ids = [f.followed_id for f in current_user.following]
        tag_ids = [t.tag_id for t in current_user.tag_follows]
        posts = Post.query.filter(
            (Post.author_id.in_(followed_ids)) | (Post.tags.any(Tag.id.in_(tag_ids)))
        ).filter_by(is_published=True).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False)
    else:
        posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False)
    return render_template('blog/index.html', posts=posts)

# Follow/unfollow author
@blog_bp.route('/user/<int:user_id>/follow', methods=['POST'])
@login_required
def follow_user(user_id):
    if user_id == current_user.id:
        return jsonify({'status': 'error', 'message': 'Cannot follow yourself.'}), 400
    user = User.query.get_or_404(user_id)
    if not Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first():
        follow = Follow(follower_id=current_user.id, followed_id=user_id)
        db.session.add(follow)
        db.session.commit()
        return jsonify({'status': 'followed'})
    return jsonify({'status': 'already-following'})

@blog_bp.route('/user/<int:user_id>/unfollow', methods=['POST'])
@login_required
def unfollow_user(user_id):
    follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'status': 'unfollowed'})
    return jsonify({'status': 'not-following'})

# Follow/unfollow tag
@blog_bp.route('/tag/<int:tag_id>/follow', methods=['POST'])
@login_required
def follow_tag(tag_id):
    if not UserTagFollow.query.filter_by(user_id=current_user.id, tag_id=tag_id).first():
        follow = UserTagFollow(user_id=current_user.id, tag_id=tag_id)
        db.session.add(follow)
        db.session.commit()
        return jsonify({'status': 'followed'})
    return jsonify({'status': 'already-following'})

@blog_bp.route('/tag/<int:tag_id>/unfollow', methods=['POST'])
@login_required
def unfollow_tag(tag_id):
    follow = UserTagFollow.query.filter_by(user_id=current_user.id, tag_id=tag_id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'status': 'unfollowed'})
    return jsonify({'status': 'not-following'})

@blog_bp.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    return render_template('blog/post.html', post=post, form=form)

@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                   content=form.content.data,
                   excerpt=form.excerpt.data,
                   is_published=form.is_published.data,
                   author=current_user)
        
        # Handle tags
        tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            post.tags.append(tag)
            
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog.post', id=post.id))
    return render_template('blog/create_post.html', form=form)

@blog_bp.route('/posts')
@login_required
def my_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=current_user).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('blog/my_posts.html', posts=posts)
    

@blog_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('You can only edit your own posts.', 'error')
        return redirect(url_for('blog.post', id=id))
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.excerpt = form.excerpt.data
        post.is_published = form.is_published.data
        
        # Update tags
        post.tags.clear()
        tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            post.tags.append(tag)
            
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('blog.post', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.excerpt.data = post.excerpt
        form.is_published.data = post.is_published
        form.tags.data = ', '.join([tag.name for tag in post.tags])
    return render_template('blog/edit_post.html', form=form)

@blog_bp.route('/delete/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('You can only delete your own posts.', 'error')
        return redirect(url_for('blog.post', id=id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('blog.index'))


# Upvote a comment
@blog_bp.route('/comment/<int:comment_id>/upvote', methods=['POST'])
@login_required
def upvote_comment(comment_id):
    from models import Comment
    comment = Comment.query.get_or_404(comment_id)
    if not CommentUpvote.query.filter_by(user_id=current_user.id, comment_id=comment_id).first():
        upvote = CommentUpvote(user_id=current_user.id, comment_id=comment_id)
        db.session.add(upvote)
        db.session.commit()
        return jsonify({'status': 'upvoted'})
    return jsonify({'status': 'already-upvoted'})

@blog_bp.route('/comment/<int:comment_id>/unupvote', methods=['POST'])
@login_required
def unupvote_comment(comment_id):
    upvote = CommentUpvote.query.filter_by(user_id=current_user.id, comment_id=comment_id).first()
    if upvote:
        db.session.delete(upvote)
        db.session.commit()
        return jsonify({'status': 'unupvoted'})
    return jsonify({'status': 'not-upvoted'})

# Award badge to user (admin only, for demo)
@blog_bp.route('/user/<int:user_id>/badge/<int:badge_id>/award', methods=['POST'])
@login_required
def award_badge(user_id, badge_id):
    # TODO: Add admin/permission check
    if not UserBadge.query.filter_by(user_id=user_id, badge_id=badge_id).first():
        user_badge = UserBadge(user_id=user_id, badge_id=badge_id)
        db.session.add(user_badge)
        db.session.commit()
        return jsonify({'status': 'awarded'})
    return jsonify({'status': 'already-has-badge'})

# Trending posts widget endpoint
@blog_bp.route('/trending')
def trending_posts():
    # sample: trending by most reactions in last 7 days
    trending = Post.query.outerjoin(Reaction).filter(
        Post.is_published == True
    ).group_by(Post.id).order_by(func.count(Reaction.id).desc()).limit(5).all()
    return render_template('blog/_trending.html', posts=trending)

@blog_bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    if query:
        posts = Post.query.filter(
            or_(
                Post.title.ilike(f'%{query}%'),
                Post.content.ilike(f'%{query}%'),
                Post.tags.any(Tag.name.ilike(f'%{query}%'))
            )
        ).filter_by(is_published=True).paginate(
            page=page, per_page=10, error_out=False)
    else:
        posts = Post.query.filter_by(is_published=True).paginate(
            page=page, per_page=10, error_out=False)
    return render_template('blog/search.html', posts=posts, query=query)

@blog_bp.route('/tag/<string:name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = tag.posts.filter_by(is_published=True).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('blog/tag.html', tag=tag, posts=posts)

@blog_bp.route('/post/<int:id>/react', methods=['POST'])
@login_required
def react_to_post(id):
    post = Post.query.get_or_404(id)
    reaction_type = request.form.get('type')
    emoji = request.form.get('emoji')
    
    existing_reaction = Reaction.query.filter_by(
        user=current_user, post=post).first()
        
    if existing_reaction:
        if existing_reaction.type == reaction_type and existing_reaction.emoji == emoji:
            db.session.delete(existing_reaction)
            db.session.commit()
            return jsonify({'status': 'removed'})
        else:
            existing_reaction.type = reaction_type
            existing_reaction.emoji = emoji
            db.session.commit()
            return jsonify({'status': 'updated'})
    else:
        reaction = Reaction(type=reaction_type,
                          emoji=emoji,
                          user=current_user,
                          post=post)
        db.session.add(reaction)
        db.session.commit()
        return jsonify({'status': 'added'})