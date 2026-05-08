from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class CartItems(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("cart.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)