from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import User
from app.models.chunk import Chunk

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String, unique=True, nullable=False)
    raw_html = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    cover_url = Column(String)
    aspect_ratio = Column(Float)
    title = Column(String, nullable=False)
    summary = Column(Text)
    summary_short = Column(Text)
    has_vector_summary = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_removed = Column(Boolean, default=False)
    
    chunks = relationship("Chunk", back_populates="article")
    
