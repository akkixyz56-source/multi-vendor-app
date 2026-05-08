from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.order import Order
from app.models.cart import Cart
from app.models.cart_item import CartItems
from app.models.product import Product
from app.models.user import User

from app.routes.auth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# =========================
# CREATE ORDER (CUSTOMER)
# =========================

@router.post("/create")
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_items = db.query(CartItems).filter(
        CartItems.cart_id == cart.id
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    order = Order(
        user_id=current_user.id,
        status="Pending",
        is_paid=False,
        is_delivered=False
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(order_item)

    db.commit()

    # clear cart after order
    for item in cart_items:
        db.delete(item)

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": order.id
    }


# =========================
# CUSTOMER ORDERS
# =========================

@router.get("/my")
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()

    return orders


# =========================
# VENDOR ORDERS
# =========================

@router.get("/vendor")
def get_vendor_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    vendor_products = db.query(Product).filter(
        Product.vendor_id == current_user.id
    ).all()

    product_ids = [p.id for p in vendor_products]

    order_items = db.query(OrderItem).filter(
        OrderItem.product_id.in_(product_ids)
    ).all()

    return order_items


# =========================
# ADMIN ALL ORDERS
# =========================

@router.get("/all")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    orders = db.query(Order).all()

    return orders


# =========================
# PAY ORDER
# =========================

@router.put("/pay/{order_id}")
def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.is_paid = True

    db.commit()

    return {
        "message": "Payment successful"
    }


# =========================
# DELIVER ORDER (ADMIN)
# =========================

@router.put("/deliver/{order_id}")
def deliver_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.is_delivered = True
    order.status = "Delivered"

    db.commit()

    return {
        "message": "Order delivered"
    }