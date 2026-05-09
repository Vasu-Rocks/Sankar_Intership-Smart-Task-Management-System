import os
import psycopg2
from psycopg2 import pool

db_pool = None

def init_db_pool():
    global db_pool
    if not db_pool:
        try:
            db_pool = psycopg2.pool.ThreadedConnectionPool(
                1, 20,
                host=os.environ.get('DB_HOST'),
                database=os.environ.get('DB_NAME'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD')
            )
            print("Database connection pool created successfully")
        except Exception as e:
            print(f"Error creating connection pool: {e}")

def get_db_connection():
    try:
        if db_pool:
            return db_pool.getconn()
        else:
            print("Connection pool is not initialized.")
            return None
    except Exception as e:
        print(f"Error getting connection from pool: {e}")
        return None

def release_db_connection(conn):
    try:
        if db_pool and conn:
            db_pool.putconn(conn)
    except Exception as e:
        print(f"Error releasing connection to pool: {e}")
