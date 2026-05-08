from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.cart import Cart
from app.models.cart_item import CartItems
from app.models.product import Product
from app.schemas.cart import AddToCart
from app.core.deps import require_role

router = APIRouter(prefix="/cart", tags=["Cart"])


# 🛒 Add to Cart (Customer only)
@router.post("/add")
def add_to_cart(
    item: AddToCart,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer"))
):
    # get or create cart
    cart = db.query(Cart).filter(Cart.user_id == user["user_id"]).first()

    if not cart:
        cart = Cart(user_id=user["user_id"])
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # check product
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # add item
    cart_item = CartItems(
        cart_id=cart.id,
        product_id=item.product_id,
        quantity=item.quantity
    )

    db.add(cart_item)
    db.commit()

    return {"message": "Added to cart"}
    

# 📦 View Cart
@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    user=Depends(require_role("customer"))
):
    cart = db.query(Cart).filter(Cart.user_id == user["user_id"]).first()

    if not cart:
        return {"cart": []}

    items = db.query(CartItems).filter(CartItems.cart_id == cart.id).all()

    return items


# ❌ Remove from Cart
@router.delete("/remove/{item_id}")
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer"))
):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Removed from cart"}