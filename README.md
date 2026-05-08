# Smart Task Management System

This is a Python-based web application built with Flask, PostgreSQL, Pandas, NumPy, and WebSockets.

## Project Structure

- `app.py`: Main Flask application entry point
- `database.py`: PostgreSQL connection logic
- `schema.sql`: Database schema definition
- `templates/`: HTML templates
- `static/`: CSS and JS files

## Setup Instructions

1. Ensure PostgreSQL is installed and running on your local machine.
2. Create a database named `task_app_db` in pgAdmin.
3. Open pgAdmin, connect to `task_app_db`, and execute the SQL commands found in `schema.sql`.
4. Update the `.env` file with your PostgreSQL password.
5. Set up the Python virtual environment and install dependencies:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   ```
