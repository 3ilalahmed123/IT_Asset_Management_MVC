from flask import Flask, session, redirect, url_for, request
from flask_cors import CORS
from controllers import auth_bp, home_bp, management_bp

import sqlite3 
from db import get_db

app = Flask(__name__)
app.secret_key = 'abc123'

# Register Blueprints from Controllers 
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(home_bp, url_prefix="/home")
app.register_blueprint(management_bp, url_prefix="/management")

CORS(app)


def init_db(): 
    with app.app_context(): 
        db = get_db() 
        with app.open_resource('schema.sql', mode='r') as f: 
            db.executescript(f.read()) 
        db.commit() 


@app.cli.command('initdb') 
def initdb_command(): 
    """Initializes the database.""" 
    init_db() 
    print('Initialized the database.') 
        
        
        
@app.before_request
def check_login_status():
    # Exclude routes from login check
    excluded_routes = ["/auth/login", "/auth/signup","static"] #Static needed so js can run
    if not session.get('logged_in') and not any(route in request.path for route in excluded_routes):
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in
    elif session.get('logged_in') and request.path == "/":
        return redirect(url_for('home.index'))  # Redirect to home if logged in

if __name__ == "__main__":
    app.run(debug=True)
