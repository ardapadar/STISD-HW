import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Docker'dan veya yerelden gelecek olan URL, yoksa default postgres'e bağlan
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:1234@localhost:5432/microdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Veritabanı oturumu açıp kapatmak için yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()