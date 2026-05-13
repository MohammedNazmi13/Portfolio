from app import create_app
from models import db
from models.models import User
from werkzeug.security import generate_password_hash

def update_admin():
    app = create_app()
    with app.app_context():
        user = User.query.first()
        if user:
            user.username = "MD Nazmi"
            user.password = generate_password_hash("Nazmi@130505")
            db.session.commit()
            print("Admin credentials updated successfully!")
        else:
            # If no user exists, create one
            new_user = User(
                username="MD Nazmi",
                password=generate_password_hash("Nazmi@130505")
            )
            db.session.add(new_user)
            db.session.commit()
            print("New admin user created successfully!")

if __name__ == "__main__":
    update_admin()
