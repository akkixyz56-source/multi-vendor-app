from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from .config import SECRET_KEY, ALGORITHM

# 🔐 Secret config (same as auth.py)
SECRET_KEY = "secret123"
ALGORITHM = "HS256"

# 🔒 Swagger auth scheme
security = HTTPBearer()


# ✅ Get current user from token
def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ✅ Role-based access control
def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker