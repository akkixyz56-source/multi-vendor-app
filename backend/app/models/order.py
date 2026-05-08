# app/models/order.py

from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    vendor_id = Column(Integer)   # 🔥 important
    product_id = Column(Integer)
    quantity = Column(Integer)

    status = Column(String, default="placed")  
    # placed → shipped → delivered

    payment_status = Column(String, default="paid")