import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def migrate():
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', 'root')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_name = os.environ.get('DB_NAME', 'portfolio_db')

    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:
            # Check if issuer column is NOT NULL
            cursor.execute("DESCRIBE certificates")
            columns = cursor.fetchall()
            for col in columns:
                if col[0] == 'issuer':
                    if col[2] == 'NO': # NO means NOT NULL
                        print("Making issuer column nullable...")
                        cursor.execute("ALTER TABLE certificates MODIFY issuer VARCHAR(150) NULL")
                        print("Success.")
                    else:
                        print("issuer column is already nullable.")
            
        connection.commit()
    finally:
        connection.close()

if __name__ == '__main__':
    migrate()
