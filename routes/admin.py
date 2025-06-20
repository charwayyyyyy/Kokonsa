from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Post, Comment, Tag, db
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'error')
            return redirect(url_for('blog.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_comments = Comment.query.count()
    pending_comments = Comment.query.filter_by(is_approved=False).count()
    
    return render_template('admin/index.html',
                         total_users=total_users,
                         total_posts=total_posts,
                         total_comments=total_comments,
                         pending_comments=pending_comments)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users)

@admin_bp.route('/user/<int:id>/toggle-admin')
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash('You cannot change your own admin status.', 'error')
    else:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f'Admin status for {user.username} has been updated.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/posts')
@login_required
@admin_required
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/posts.html', posts=posts)

@admin_bp.route('/post/<int:id>/toggle-publish')
@login_required
@admin_required
def toggle_publish(id):
    post = Post.query.get_or_404(id)
    post.is_published = not post.is_published
    db.session.commit()
    flash(f'Post "{post.title}" has been {"published" if post.is_published else "unpublished"}.', 'success')
    return redirect(url_for('admin.posts'))

@admin_bp.route('/comments')
@login_required
@admin_required
def comments():
    page = request.args.get('page', 1, type=int)
    filter_approved = request.args.get('approved')
    
    query = Comment.query
    if filter_approved is not None:
        query = query.filter_by(is_approved=(filter_approved == 'true'))
        
    comments = query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/comments.html', comments=comments)

@admin_bp.route('/comment/<int:id>/toggle-approve')
@login_required
@admin_required
def toggle_approve(id):
    comment = Comment.query.get_or_404(id)
    comment.is_approved = not comment.is_approved
    db.session.commit()
    flash(f'Comment has been {"approved" if comment.is_approved else "unapproved"}.', 'success')
    return redirect(url_for('admin.comments'))

@admin_bp.route('/comment/<int:id>/delete')
@login_required
@admin_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been deleted.', 'success')
    return redirect(url_for('admin.comments'))

@admin_bp.route('/tags')
@login_required
@admin_required
def tags():
    tags = Tag.query.all()
    return render_template('admin/tags.html', tags=tags)

@admin_bp.route('/tag/<int:id>/delete')
@login_required
@admin_required
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash(f'Tag "{tag.name}" has been deleted.', 'success')
    return redirect(url_for('admin.tags'))