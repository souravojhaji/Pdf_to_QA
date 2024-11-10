import uuid
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://pdf_user:your_password@localhost/pdf_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PDFDocument(Base):
    __tablename__ = "pdf_documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)  # Use Text for larger content

def init_db():
    Base.metadata.create_all(bind=engine)
