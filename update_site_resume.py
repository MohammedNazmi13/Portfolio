import pymysql
from config import Config

def update_site_content_address_resume():
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        print("Adding address and resume columns to site_content table...")
        
        # Add address
        try:
            cursor.execute("ALTER TABLE site_content ADD COLUMN address VARCHAR(255) NULL;")
            print("Added address column.")
        except Exception as e:
            print(f"address column might already exist: {e}")

        # Add resume_url
        try:
            cursor.execute("ALTER TABLE site_content ADD COLUMN resume_url VARCHAR(255) NULL;")
            print("Added resume_url column.")
        except Exception as e:
            print(f"resume_url column might already exist: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        print("Database update for site_content complete.")
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == '__main__':
    update_site_content_address_resume()
