from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.core.deps import require_role

router = APIRouter(prefix="/products", tags=["Products"])


# ✅ ADD PRODUCT (Vendor Only)
@router.post("/")
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("vendor"))
):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        vendor_id=user["user_id"]
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product added successfully",
        "product": new_product
    }


# ✅ GET PRODUCTS (Search + Filter + Pagination)
@router.get("/")
def get_products(
    search: str = "",
    min_price: float = 0,
    max_price: float = 1000000,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    # 🔍 Search
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # 💰 Price filter
    query = query.filter(Product.price >= min_price)
    query = query.filter(Product.price <= max_price)

    # 📄 Pagination
    offset = (page - 1) * limit
    products = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "data": products
    }


# ✅ GET SINGLE PRODUCT
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# ✅ UPDATE PRODUCT (Vendor Only + Ownership)
@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("vendor"))
):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if db_product.vendor_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="You can only update your own products")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.stock = product.stock

    db.commit()
    db.refresh(db_product)

    return {
        "message": "Product updated successfully",
        "product": db_product
    }


# ✅ DELETE PRODUCT (Vendor Only + Ownership)
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("vendor"))
):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if db_product.vendor_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="You can only delete your own products")

    db.delete(db_product)
    db.commit()

    return {"message": "Product deleted successfully"}