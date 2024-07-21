from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Chunk(Base):
    __tablename__ = 'chunks'
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    content = Column(String, nullable=False)
    url = Column(String, nullable=False)
    has_vector = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_removed = Column(Boolean, default=False)

    
    article = relationship("Article", back_populates="chunks")
