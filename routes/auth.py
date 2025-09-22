from flask import Blueprint, render_template, redirect, url_for, flash
from forms import RegisterForm, LoginForm
from models.user import User
from utils.db import db
from flask_login import login_user, login_required, logout_user, current_user
from extensions import bcrypt


auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return render_template('home.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    forms = RegisterForm()

    if forms.validate_on_submit():
        existing_username = User.query.filter_by(username = forms.username.data).first()
        if existing_username:
            flash('Username already exist. Please choose another', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(forms.password.data).decode("utf-8")
            new_user = User(username = forms.username.data, password = hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. Please log in', 'success')
            return redirect(url_for('auth.login'))


    return render_template('register.html', forms = forms)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    forms = LoginForm()

    if forms.validate_on_submit():
        user = User.query.filter_by(username=forms.username.data).first()
        if not user:
            flash('Username not found', 'error')
        elif not bcrypt.check_password_hash(user.password, forms.password.data):
            flash('Incorrect Password', 'error')
        else:
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('auth.dashboard'))

    return render_template('login.html', forms = forms)

@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('auth.login', user = current_user))