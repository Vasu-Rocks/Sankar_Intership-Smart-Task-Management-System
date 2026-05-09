import psycopg2.extras
from flask import Blueprint, request, session, jsonify
from functools import wraps
from extensions import socketio
from database import get_db_connection, release_db_connection

tasks_bp = Blueprint('tasks', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@tasks_bp.route('/', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Bad Request: Title is required'}), 400

    title = data.get('title')
    description = data.get('description', '')
    priority = data.get('priority', 'Medium')
    status = data.get('status', 'Pending')
    user_id = session['user_id']

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO tasks (user_id, title, description, priority, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            ''',
            (user_id, title, description, priority, status)
        )
        new_task_id = cursor.fetchone()[0]
        conn.commit()
        socketio.emit('task_updated', room=str(user_id))
        return jsonify({'message': 'Task created successfully', 'id': new_task_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500
    finally:
        if cursor:
            cursor.close()
        release_db_connection(conn)

@tasks_bp.route('/', methods=['GET'])
@login_required
def get_all_tasks():
    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            'SELECT id, title, description, priority, status, created_date FROM tasks WHERE user_id = %s ORDER BY created_date DESC',
            (user_id,)
        )
        tasks = cursor.fetchall()
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
    finally:
        if cursor:
            cursor.close()
        release_db_connection(conn)

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Bad Request: No data provided'}), 400

    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = None
    try:
        cursor = conn.cursor()
        
        # Build dynamic query
        fields = []
        values = []
        for key in ['title', 'description', 'priority', 'status']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])
                
        if not fields:
            return jsonify({'error': 'Bad Request: No updatable fields provided'}), 400

        values.extend([task_id, user_id])
        
        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = %s AND user_id = %s"
        
        cursor.execute(query, tuple(values))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Not Found or Unauthorized'}), 404
            
        conn.commit()
        socketio.emit('task_updated', room=str(user_id))
        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500
    finally:
        if cursor:
            cursor.close()
        release_db_connection(conn)

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM tasks WHERE id = %s AND user_id = %s RETURNING id',
            (task_id, user_id)
        )
        
        deleted_id = cursor.fetchone()
        if not deleted_id:
            return jsonify({'error': 'Not Found or Unauthorized'}), 404
            
        conn.commit()
        socketio.emit('task_updated', room=str(user_id))
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500
    finally:
        if cursor:
            cursor.close()
        release_db_connection(conn)
