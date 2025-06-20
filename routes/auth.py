from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from models import User, db
from forms.auth import LoginForm, RegistrationForm, ProfileForm
from werkzeug.utils import secure_filename
import os

auth_bp = Blueprint('auth', __name__)

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
            filename = secure_filename(form.avatar.data.filename)
            form.avatar.data.save(os.path.join('static', 'avatars', filename))
            current_user.avatar = filename
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.bio.data = current_user.bio
    return render_template('auth/profile.html', title='Profile', form=form)