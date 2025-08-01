from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Using SQLAlchemy recommended URL format for PostgreSQL
DATABASE_URL = 'postgresql://postgres:md1234@localhost:5432/musicapp'

# Create database engine with connection pooling and logging
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    