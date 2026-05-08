from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))