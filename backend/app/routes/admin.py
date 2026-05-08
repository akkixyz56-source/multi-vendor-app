from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.core.deps import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


# 👥 View all users
@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return db.query(User).all()


# 📦 View all products
@router.get("/products")
def get_products(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return db.query(Product).all()


# 🧾 View all orders
@router.get("/orders")
def get_orders(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return db.query(Order).all()


# ❌ Delete any product
@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"message": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Product deleted by admin"}