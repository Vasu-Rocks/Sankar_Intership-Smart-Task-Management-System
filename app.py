import os
from datetime import timedelta
from flask import Flask, redirect, url_for, session, render_template, flash
from flask_socketio import join_room
from dotenv import load_dotenv

# Import database and blueprints
from database import init_db_pool
from extensions import socketio
from routes.auth_routes import auth_bp
from routes.task_routes import tasks_bp
from routes.analytics_routes import analytics_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Load the secret key from the environment variable securely
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Configure session lifetime
app.permanent_session_lifetime = timedelta(hours=2)

# Initialize Database Connection Pool
with app.app_context():
    init_db_pool()

socketio.init_app(app)

@socketio.on('connect')
def handle_connect():
    if 'user_id' in session:
        join_room(str(session['user_id']))

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('auth.login'))
    
    return render_template('dashboard.html', username=session['username'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
