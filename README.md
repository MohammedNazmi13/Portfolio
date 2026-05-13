# Full-Stack Dynamic Portfolio Web Application

A production-ready, full-stack portfolio designed for a Backend Developer. Built with Python, Flask, MySQL, and vanilla front-end technologies.

## Features

*   **Public Portfolio:** Fully responsive dark theme UI with smooth scroll animations.
*   **Dynamic Projects:** Projects are fetched via a REST API from the database.
*   **Admin Panel:** Secure, session-based authentication to manage projects (CRUD operations).
*   **Contact Form:** Submits messages directly to the database.

## Prerequisites

*   Python 3.8+
*   MySQL Server running locally or remotely

## Setup Instructions

1.  **Clone the repository / Navigate to the directory:**
    ```bash
    cd portfolio_app
    ```

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    *   Copy the `.env.example` file to `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Open `.env` and verify your MySQL database credentials:
        ```env
        SECRET_KEY=your-super-secret-key
        DB_USER=root
        DB_PASSWORD=root
        DB_HOST=localhost
        DB_NAME=portfolio_db
        ```

5.  **Initialize the Database:**
    Run the setup script. This will create the database, tables, and the default admin user.
    ```bash
    python init_db.py
    ```

6.  **Run the Application:**
    ```bash
    python app.py
    ```
    The app will start on `http://127.0.0.1:5000/`.

## Usage

*   **Public Site:** Visit `http://127.0.0.1:5000/` to see the portfolio.
*   **Admin Dashboard:** Visit `http://127.0.0.1:5000/admin/login`
    *   **Default Username:** `admin`
    *   **Default Password:** `admin123`
    *   Once logged in, you can Add, Edit, and Delete projects.

## Project Structure
*   `/routes`: Contains API, Admin, and Public routing logic.
*   `/models`: SQLAlchemy models (`User`, `Project`, `Contact`).
*   `/templates`: HTML views (Jinja2 templates).
*   `/static`: CSS, JavaScript, and Images.
