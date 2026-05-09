<a id="readme-top"></a>

<div align="center">
  <h3 align="center">Smart Task Management System</h3>

  <p align="center">
    A full-stack, real-time task management web application built for the Sankar Group Python Development Internship Assignment.
    <br />
    <a href="#"><strong>Explore the repository »</strong></a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#database-setup">Database Setup</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This is a production-grade, real-time Task Management Web Application built to evaluate core competencies in Python backend development, asynchronous frontend orchestration, and in-memory data processing.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Features

* **Secure Authentication:** User registration and login with encrypted password hashing (Werkzeug) and secure Flask sessions.
* **RESTful API:** Robust JSON endpoints for all Task CRUD operations, protected by user-specific database isolation.
* **Real-Time Synchronization:** WebSockets via Flask-SocketIO push live updates across all active user sessions instantly.
* **Data Analytics:** In-memory data processing using Pandas and NumPy to calculate task completion metrics safely and efficiently.
* **SPA-Lite Frontend:** A dynamic, responsive dashboard built with Bootstrap 5, custom Glassmorphism CSS, and asynchronous JavaScript (Fetch API).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
* [![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
* [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
* [![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
* [![Socket.io](https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://socket.io/)
* [![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

* Python 3.8+ installed
* PostgreSQL & pgAdmin installed and running locally

### Database Setup

1. Open pgAdmin or your PostgreSQL CLI.
2. Create a new database named `task_app_db`.
3. Execute the provided `schema.sql` file within this database to generate the `users` and `tasks` tables.

### Installation

1. Clone this repository and navigate to the project root.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your credentials:
   ```env
   DB_HOST=localhost
   DB_NAME=task_app_db
   DB_USER=postgres
   DB_PASSWORD=your_database_password_here
   FLASK_SECRET_KEY=your_secure_random_secret_key
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage

1. Start the Flask-SocketIO server:
   ```bash
   python app.py
   ```
2. Navigate to `http://127.0.0.1:5000` in your web browser.
3. Register a new user account, log in, and experience the real-time SPA dashboard!

<p align="right">(<a href="#readme-top">back to top</a>)</p>
