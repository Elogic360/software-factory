"""
Universal JWT & RBAC Auth Core Reference Implementation
"""
import time
from typing import Dict, List, Optional
import jwt

SECRET_KEY = "software-factory-demo-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta_seconds: int = 3600) -> str:
    to_encode = data.copy()
    expire = time.time() + expires_delta_seconds
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None

def check_permission(user_roles: List[str], required_role: str) -> bool:
    if "admin" in user_roles:
        return True
    return required_role in user_roles
