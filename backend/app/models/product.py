from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    vendor_id = Column(Integer, ForeignKey("users.id"))