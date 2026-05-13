import pymysql
from config import Config

def update_database():
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        print(f"Adding demo_link column to projects table...")
        cursor.execute("ALTER TABLE projects ADD COLUMN demo_link VARCHAR(255) NULL;")
        conn.commit()
        cursor.close()
        conn.close()
        print("Database updated.")
    except Exception as e:
        print(f"Error updating database (might already have the column): {e}")

if __name__ == '__main__':
    update_database()
