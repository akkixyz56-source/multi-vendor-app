import re

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routes import auth, products, cart, orders, admin, reviews
from app.deps import get_current_user

app = FastAPI()

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(reviews.router)

# ========================
# ✅ BASIC ROUTES
# ========================

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


# ========================
# 🔐 AUTH / ROLE TEST ROUTES
# ========================

# 🔓 Protected (any logged-in user)
@app.get("/protected")
def protected(current_user=Depends(get_current_user)):
    return {
        "message": "Authorized",
        "user": current_user
    }


# 🧑‍💼 Vendor only
@app.get("/vendor-only")
def vendor_dashboard(user=Depends((get_current_user))):
    return {"message": "Welcome Vendor"}


# 🛠 Admin only
@app.get("/admin-only")
def admin_dashboard(user=Depends(get_current_user)):
    return {"message": "Welcome Admin"}


# 🛒 Customer only
@app.get("/customer-only")
def customer_area(user=Depends(get_current_user)):
    return {"message": "Welcome Customer"}