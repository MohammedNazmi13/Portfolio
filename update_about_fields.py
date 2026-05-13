import pymysql
from config import Config

def update_db():
    print(f"Connecting to MySQL database {Config.DB_NAME}...")
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()

        # Add new columns to site_content table
        columns_to_add = [
            ('about_initials', 'VARCHAR(10)'),
            ('looking_for_1', 'VARCHAR(100)'),
            ('looking_for_2', 'VARCHAR(100)'),
            ('stat1_value', 'VARCHAR(50)'),
            ('stat1_label', 'VARCHAR(50)'),
            ('stat2_value', 'VARCHAR(50)'),
            ('stat2_label', 'VARCHAR(50)'),
            ('stat3_value', 'VARCHAR(50)'),
            ('stat3_label', 'VARCHAR(50)'),
            ('section1_title', 'VARCHAR(100)'),
            ('section1_desc', 'TEXT'),
            ('section2_title', 'VARCHAR(100)'),
            ('section2_desc', 'TEXT'),
            ('section3_title', 'VARCHAR(100)'),
            ('section3_desc', 'TEXT')
        ]

        for col_name, col_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE site_content ADD COLUMN {col_name} {col_type}")
                print(f"Added column {col_name}")
            except Exception as e:
                print(f"Column {col_name} might already exist or error: {e}")

        # Update data with new defaults
        cursor.execute("""
            UPDATE site_content SET 
            about_title = 'Building Intelligent Solutions',
            about_subtitle = 'ABOUT ME',
            about_initials = 'MN',
            looking_for_1 = 'Full-Stack Developer',
            looking_for_2 = 'Backend Systems',
            stat1_value = '2+',
            stat1_label = 'Years Coding',
            stat2_value = '10+',
            stat2_label = 'Projects Built',
            stat3_value = '∞',
            stat3_label = 'Curiosity',
            section1_title = 'Vision',
            section1_desc = 'Passionate about building scalable and impactful digital solutions.',
            section2_title = 'Approach',
            section2_desc = 'Focused on clean architecture, performance, and intelligent systems.',
            section3_title = 'Current Focus',
            section3_desc = 'Exploring backend systems, analytics, and AI-driven applications.'
            WHERE id = 1
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Database updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_db()
