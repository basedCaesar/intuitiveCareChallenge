import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
dbname = os.getenv('DB_NAME')

if not all([user, password, host, port, dbname]):
    print("ALERTA: Algumas variáveis de ambiente do banco de dados estão faltando!")

DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
print(f"Conectando em: postgresql://{user}:***@{host}:{port}/{dbname}") # Log de debug

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Erro de conexão na sessão: {e}")
        raise
    finally:
        db.close()