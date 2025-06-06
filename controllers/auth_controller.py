from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify, flash
from models.auth_model import attempt_login, register_user
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST']) #Auth/Login to log in
def login():
    if 'logged_in' in session:
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = attempt_login(username, password)
        if user:
            session['logged_in'] = True
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            return jsonify({"message": "Login successful", "redirect": "/home"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    return render_template('login.html')



@auth_bp.route('/signup', methods=['GET', 'POST']) #Signup Account
def signup():
    if request.method == 'POST':
        data = request.get_json()
        forename = data.get("forename")
        surname = data.get("surname")
        username = data.get("username")
        password = data.get("password")

        # Validate password
        if len(password) < 8 or not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$", password):
            return jsonify({"message": "Password must be at least 8 characters long and alphanumeric"}), 400

        # Register the user
        user = register_user(forename, surname, username, password)
        if user:
            print(user)
            session['logged_in'] = True
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            return jsonify({"message": "Signup successful", "redirect": "/home"}), 200
        else:
            return jsonify({"message": "Signup failed. Username might already be taken."}), 400

    return render_template('login.html')

#Auth/Logout to log out
@auth_bp.route('logout') 
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

