"""
Universal User Management Service Raw Material.
Provides production-ready user lifecycle: registration, profile updates,
status management (ACTIVE, SUSPENDED), and role assignment.
"""

import time
import uuid
from typing import Dict, List, Any, Optional

class UserService:
    """Manages user identity lifecycle and profile attributes."""

    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}

    def register_user(self, email: str, full_name: str, roles: Optional[List[str]] = None) -> Dict[str, Any]:
        email_clean = email.strip().lower()
        for u in self.users.values():
            if u["email"] == email_clean:
                raise ValueError(f"User with email '{email_clean}' already exists.")

        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        user_record = {
            "id": user_id,
            "email": email_clean,
            "full_name": full_name,
            "roles": roles or ["user"],
            "status": "ACTIVE",
            "mfa_enabled": False,
            "created_at": time.time(),
            "updated_at": time.time()
        }
        self.users[user_id] = user_record
        return user_record

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users.get(user_id)

    def update_profile(self, user_id: str, full_name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User '{user_id}' not found.")
        if full_name:
            user["full_name"] = full_name
        if metadata:
            user.setdefault("metadata", {}).update(metadata)
        user["updated_at"] = time.time()
        return user

    def set_status(self, user_id: str, status: str) -> Dict[str, Any]:
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User '{user_id}' not found.")
        if status not in ["ACTIVE", "SUSPENDED", "DEACTIVATED"]:
            raise ValueError(f"Invalid user status: '{status}'.")
        user["status"] = status
        user["updated_at"] = time.time()
        return user
