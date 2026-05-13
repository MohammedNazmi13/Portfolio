import pymysql
from config import Config

def update_database():
    print("Connecting to MySQL server...")
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        print(f"Adding image_url column to projects table...")
        try:
            cursor.execute("ALTER TABLE projects ADD COLUMN image_url VARCHAR(255) AFTER demo_link;")
            conn.commit()
            print("Column added successfully.")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("Column already exists.")
            else:
                print(f"Error adding column: {e}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")

if __name__ == '__main__':
    update_database()
