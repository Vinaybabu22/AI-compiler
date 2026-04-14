from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from .models import User
from . import db, login_manager

# 1. Initialize Blueprint and Bcrypt
auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# 2. Required for Flask-Login to find the user in the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- REGISTRATION ROUTE ---
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user already exists
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists!', category='error')
            return redirect(url_for('auth.register'))

        # Hash the password for security
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit() # Saves to compiler.db
        
        flash('Account created! Please login.', category='success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

# --- LOGIN ROUTE ---
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password matches hashed version
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('compiler.index'))
        else:
            flash('Login failed. Check username and password.', category='error')
            
    return render_template('login.html')

# --- LOGOUT ROUTE ---
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))