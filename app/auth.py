from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
import re

auth = Blueprint('auth', __name__)

# Password strength check function
def is_password_strong(password):
    if (len(password) < 8 or
            not re.search(r"[A-Za-z]", password) or
            not re.search(r"[0-9]", password) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True

# Email validation function
def is_valid_email(email):
    if email is None:  # Check for None
        return False
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Change from username to email
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False  # Check if remember me is checked
        user = User.query.filter_by(email=email).first()  # Query by email
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)  # Pass remember parameter
            flash('Logged in successfully!', category='success')
            return redirect(url_for('main.home'))  # Adjust to your actual home route
        else:
            flash('Login failed. Check email and password.', category='error')
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')  # Capture confirmation password

        # Debugging output
        print(f"Email: {email}, Username: {username}, Password: {password}, Confirm Password: {confirm_password}")

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', category='error')
            return redirect(url_for('auth.register'))

        # Check for an existing user with the same email
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists. Please choose another.', category='error')
            return redirect(url_for('auth.register'))

        # Validate email format
        if email is None or not is_valid_email(email):
            flash('Please enter a valid email address.', category='error')
            return redirect(url_for('auth.register'))

        # Check password strength
        if not is_password_strong(password):
            flash('Password must be at least 8 characters long and include letters, numbers, and special characters.', category='error')
            return redirect(url_for('auth.register'))

        # Create new user with a hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', category='success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('auth.login'))
