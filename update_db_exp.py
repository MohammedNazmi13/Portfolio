from app import create_app
from models import db
from models.models import Experience

app = create_app()
with app.app_context():
    db.create_all()
    print("Experience table created successfully!")
