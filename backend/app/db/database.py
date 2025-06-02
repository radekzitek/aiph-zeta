from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

logger.debug(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
logger.debug(f"SQLAlchemy engine created: {engine}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.debug(f"SessionLocal configured: {SessionLocal}")


def get_db():
    logger.debug("Creating new database session.")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.debug("Closing database session.")
        db.close()
