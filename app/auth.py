from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
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

# --- PROFILE ROUTE ---
@auth.route('/profile')
@login_required
def profile():
    from .models import CodeHistory
    from datetime import datetime, timedelta
    from collections import Counter
    codes = CodeHistory.query.filter_by(user_id=current_user.id).order_by(CodeHistory.timestamp.desc()).all()

    total_saved  = len(codes)
    lang_set     = list(set(c.language for c in codes))
    langs_used   = len(lang_set)

    week_ago     = datetime.utcnow() - timedelta(days=7)
    recent_count = sum(1 for c in codes if c.timestamp >= week_ago)
    recent_codes = codes[:5]

    # Count per language for breakdown bars
    lang_counts  = dict(Counter(c.language for c in codes))

    return render_template(
        'profile.html',
        total_saved   = total_saved,
        langs_used    = langs_used,
        recent_count  = recent_count,
        language_list = lang_set,
        recent_codes  = recent_codes,
        lang_counts   = lang_counts,
    )