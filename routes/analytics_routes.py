import psycopg2.extras
import pandas as pd
import numpy as np
from flask import Blueprint, session, jsonify
from routes.task_routes import login_required
from database import get_db_connection, release_db_connection

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/', methods=['GET'])
@login_required
def get_analytics():
    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # Fetch only the status column for performance
        cursor.execute('SELECT status FROM tasks WHERE user_id = %s', (user_id,))
        tasks = cursor.fetchall()
        
        # Early exit if there are no tasks
        if not tasks:
            return jsonify({
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'completion_percentage': 0.0
            }), 200

        # Load data into a Pandas DataFrame
        df = pd.DataFrame(tasks)

        # Calculate metrics
        total_tasks = len(df)
        completed_tasks = (df['status'] == 'Completed').sum()
        pending_tasks = (df['status'] == 'Pending').sum()

        # Calculate percentage using numpy to avoid division by zero
        completion_percentage = np.where(
            total_tasks > 0,
            (completed_tasks / total_tasks) * 100,
            0.0
        )
        completion_percentage = round(float(completion_percentage), 2)

        # Convert numpy types back to standard python types for JSON serialization
        return jsonify({
            'total_tasks': int(total_tasks),
            'completed_tasks': int(completed_tasks),
            'pending_tasks': int(pending_tasks),
            'completion_percentage': float(completion_percentage)
        }), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
    finally:
        if cursor:
            cursor.close()
        release_db_connection(conn)
