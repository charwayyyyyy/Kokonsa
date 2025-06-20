from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import Post, Comment, Tag, Reaction, db
from forms.blog import PostForm, CommentForm
from markdown import markdown
from sqlalchemy import or_

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('blog/index.html', posts=posts)

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

@blog_bp.route('/post/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data,
                        author=current_user,
                        post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('blog.post', id=id))

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