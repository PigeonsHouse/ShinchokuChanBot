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

url = os.environ.get('DATABASE_URL')
if url is None or url == '':
	DATABASE_URL = f"{DATABASE}://{HOST}:{PORT}/{DB_NAME}?user={USER}&password={PASSWORD}"
else:
	DATABASE_URL = url.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
