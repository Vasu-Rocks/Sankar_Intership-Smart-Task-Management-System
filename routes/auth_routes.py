import psycopg2
import psycopg2.extras
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, release_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if not conn:
            flash('Database connection failed.', 'danger')
            return redirect(url_for('auth.register'))
        
        cursor = None
        try:
            cursor = conn.cursor()
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash('Username already taken.', 'warning')
        except Exception as e:
            conn.rollback()
            flash('An unexpected error occurred.', 'danger')
        finally:
            if cursor:
                cursor.close()
            release_db_connection(conn)

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed.', 'danger')
            return redirect(url_for('auth.login'))
        
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute('SELECT id, username, password_hash FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                session.permanent = True
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        except Exception as e:
            flash('An unexpected error occurred.', 'danger')
        finally:
            if cursor:
                cursor.close()
            release_db_connection(conn)

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
