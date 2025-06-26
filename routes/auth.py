from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from models import User, db
from forms.auth import LoginForm, RegistrationForm, ProfileForm
from werkzeug.utils import secure_filename
import os
# --- OAuth imports ---
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

# Register OAuth blueprints (should be done in app factory in production)
google_bp = make_google_blueprint(
    client_id=os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
    scope=["profile", "email"],
    redirect_url="/login/google/authorized"
)
github_bp = make_github_blueprint(
    client_id=os.getenv('GITHUB_OAUTH_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_OAUTH_CLIENT_SECRET'),
    redirect_url="/login/github/authorized"
)
twitter_bp = make_twitter_blueprint(
    api_key=os.getenv('TWITTER_OAUTH_CLIENT_ID'),
    api_secret=os.getenv('TWITTER_OAUTH_CLIENT_SECRET'),
    redirect_url="/login/twitter/authorized"
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('blog.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

# OAuth login routes
@auth_bp.route('/login/<provider>')
def oauth_login(provider):
    if provider == 'google':
        return redirect(url_for('google.login'))
    elif provider == 'github':
        return redirect(url_for('github.login'))
    elif provider == 'twitter':
        return redirect(url_for('twitter.login'))
    else:
        flash('Unknown OAuth provider.', 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/login/google/authorized')
def google_authorized():
    resp = google.get('/oauth2/v2/userinfo')
    if not resp.ok:
        flash('Failed to log in with Google.', 'error')
        return redirect(url_for('auth.login'))
    info = resp.json()
    email = info['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=info.get('name', email.split('@')[0]), email=email, avatar=info.get('picture'))
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Account creation failed.', 'error')
            return redirect(url_for('auth.login'))
    login_user(user)
    return redirect(url_for('blog.index'))

@auth_bp.route('/login/github/authorized')
def github_authorized():
    resp = github.get('/user')
    if not resp.ok:
        flash('Failed to log in with GitHub.', 'error')
        return redirect(url_for('auth.login'))
    info = resp.json()
    email = info.get('email')
    if not email:
        # fetch emails endpoint
        emails_resp = github.get('/user/emails')
        if emails_resp.ok:
            emails = emails_resp.json()
            email = next((e['email'] for e in emails if e['primary']), None)
    if not email:
        flash('GitHub account has no public email.', 'error')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=info.get('login', email.split('@')[0]), email=email, avatar=info.get('avatar_url'))
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Account creation failed.', 'error')
            return redirect(url_for('auth.login'))
    login_user(user)
    return redirect(url_for('blog.index'))

@auth_bp.route('/login/twitter/authorized')
def twitter_authorized():
    resp = twitter.get('account/verify_credentials.json?include_email=true')
    if not resp.ok:
        flash('Failed to log in with Twitter.', 'error')
        return redirect(url_for('auth.login'))
    info = resp.json()
    email = info.get('email')
    if not email:
        flash('Twitter account has no email.', 'error')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=info.get('screen_name', email.split('@')[0]), email=email, avatar=info.get('profile_image_url_https'))
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Account creation failed.', 'error')
            return redirect(url_for('auth.login'))
    login_user(user)
    return redirect(url_for('blog.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_folder = os.path.join('static', 'avatars')
            if not os.path.exists(avatar_folder):
                os.makedirs(avatar_folder)
            filename = secure_filename(form.avatar.data.filename)
            form.avatar.data.save(os.path.join(avatar_folder, filename))
            current_user.avatar = filename
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.bio.data = current_user.bio
    return render_template('auth/profile.html', title='Profile', form=form)