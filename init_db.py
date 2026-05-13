import pymysql
from werkzeug.security import generate_password_hash
from app import create_app
from models import db
from models.models import User, SiteContent
from config import Config

def init_database():
    # Connect to MySQL server (without specifying DB) to create the DB if it doesn't exist
    print("Connecting to MySQL server...")
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = conn.cursor()
        print(f"Creating database {Config.DB_NAME} if it doesn't exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME};")
        conn.commit()
        cursor.close()
        conn.close()
        print("Database created or already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")
        return

    # Now run Flask app context to create tables and admin user
    app = create_app()
    with app.app_context():
        print("Creating tables...")
        db.create_all()

        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            print("Creating default admin user...")
            hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
            new_admin = User(username='admin', password=hashed_pw)
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully. (username: admin, password: admin123)")
        else:
            print("Admin user already exists.")
            
        # Check if SiteContent exists
        site_content = SiteContent.query.first()
        if not site_content:
            print("Creating default site content...")
            default_content = SiteContent(
                name="Your Name",
                title="Backend Developer | Python | Flask | MySQL",
                tagline="Building scalable, secure, and performant RESTful APIs and server-side applications.",
                about="I am a passionate Backend Developer specializing in Python and Flask. I enjoy designing robust database schemas, building efficient REST APIs, and solving complex architectural problems. With a strong foundation in modern backend technologies, I focus on delivering clean, maintainable code.",
                email="hello@example.com",
                phone="+1 (555) 123-4567",
                skills="Python, Flask, MySQL, REST API, Git, Linux, HTML/CSS"
            )
            db.session.add(default_content)
            db.session.commit()
            print("Default site content created successfully.")
        else:
            print("Site content already exists.")
        
        print("Database initialization complete.")

if __name__ == '__main__':
    init_database()
