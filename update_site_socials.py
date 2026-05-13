import pymysql
from config import Config

def update_site_content_table():
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        print("Adding social links columns to site_content table...")
        
        # Add github_link
        try:
            cursor.execute("ALTER TABLE site_content ADD COLUMN github_link VARCHAR(255) NULL;")
            print("Added github_link column.")
        except Exception as e:
            print(f"github_link column might already exist: {e}")

        # Add linkedin_link
        try:
            cursor.execute("ALTER TABLE site_content ADD COLUMN linkedin_link VARCHAR(255) NULL;")
            print("Added linkedin_link column.")
        except Exception as e:
            print(f"linkedin_link column might already exist: {e}")

        # Add whatsapp
        try:
            cursor.execute("ALTER TABLE site_content ADD COLUMN whatsapp VARCHAR(50) NULL;")
            print("Added whatsapp column.")
        except Exception as e:
            print(f"whatsapp column might already exist: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        print("Database update for site_content complete.")
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == '__main__':
    update_site_content_table()
