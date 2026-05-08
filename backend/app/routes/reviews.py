from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.review import Review
from app.schemas.review import ReviewCreate
from app.core.deps import require_role

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/")
def add_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("customer"))
):
    review = Review(
        product_id=data.product_id,
        user_id=user["user_id"],
        rating=data.rating,
        comment=data.comment
    )

    db.add(review)
    db.commit()

    return {"message": "Review added"}


@router.get("/{product_id}")
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.product_id == product_id).all()