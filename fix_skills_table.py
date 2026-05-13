from app import create_app
from models.models import db
from sqlalchemy import text

app = create_app()

def add_columns():
    with app.app_context():
        # Using raw SQL to add columns to MySQL
        try:
            db.session.execute(text("ALTER TABLE skills ADD COLUMN description VARCHAR(255)"))
            print("Added description column.")
        except Exception as e:
            print(f"Description column might already exist: {e}")
            
        try:
            db.session.execute(text("ALTER TABLE skills ADD COLUMN icon_class VARCHAR(100)"))
            print("Added icon_class column.")
        except Exception as e:
            print(f"Icon_class column might already exist: {e}")
            
        db.session.commit()

if __name__ == "__main__":
    add_columns()
