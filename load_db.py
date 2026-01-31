import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    admin_url = URL.create(
        drivername="postgresql",
        username=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database="postgres"
    )
    
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    db_name = os.getenv('DB_NAME')

    with admin_engine.connect() as conn:
        exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")).fetchone()
        if not exists:
            conn.execute(text(f"CREATE DATABASE {db_name}"))

    new_db_url = admin_url._replace(database=db_name)
    engine = create_engine(new_db_url)

    # A OPÇÃO 2 ENTRA AQUI:
    with open('sql/setup_db.sql', 'r') as f:
        sql_script = f.read()

    with engine.connect() as conn:
        conn.execute(text(sql_script))
        conn.commit()
    
    print("Estrutura criada com sucesso a partir do arquivo SQL!")

if __name__ == "__main__":
    setup_database()