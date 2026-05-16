from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

def update_schema():
    with app.app_context():
        print("Updating database schema to support large image data...")
        
        # Check if we are using PostgreSQL or SQLite
        bind = db.engine.url.drivername
        print(f"Detected database driver: {bind}")
        
        tables_and_columns = [
            ('projects', 'image_url'),
            ('certificates', 'image_url'),
            ('skills', 'image_url'),
            ('site_content', 'resume_url')
        ]
        
        for table, column in tables_and_columns:
            try:
                print(f"Modifying {table}.{column} to TEXT...")
                if 'sqlite' in bind:
                    # SQLite is tricky with ALTER COLUMN, but sometimes works or we just skip if it's local
                    print("SQLite detected. Column type changes are limited, but usually String handles long text in SQLite anyway.")
                else:
                    # PostgreSQL / MySQL
                    db.session.execute(text(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE TEXT"))
                db.session.commit()
                print(f"Successfully updated {table}.{column}")
            except Exception as e:
                db.session.rollback()
                print(f"Could not update {table}.{column}: {e}")
                print("It might already be TEXT or the database doesn't support this command.")

if __name__ == '__main__':
    update_schema()
