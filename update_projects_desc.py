import pymysql
from config import Config

def update_projects_full_desc():
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        print("Adding full_description column to projects table...")
        
        try:
            cursor.execute("ALTER TABLE projects ADD COLUMN full_description TEXT NULL;")
            print("Added full_description column.")
        except Exception as e:
            print(f"full_description column might already exist: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        print("Database update for projects complete.")
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == '__main__':
    update_projects_full_desc()
