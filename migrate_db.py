import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR(100) NOT NULL DEFAULT 'User'")
cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255)")
cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

conn.commit()
print('Database migration successful! New columns: full_name, email, created_at added to users table.')
cur.close()
conn.close()
