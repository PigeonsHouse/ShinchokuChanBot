import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

DATABASE = 'postgresql'
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')
PORT = os.environ.get('POSTGRES_PORT', 5432)
DB_NAME = os.environ.get('POSTGRES_DB')

DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
