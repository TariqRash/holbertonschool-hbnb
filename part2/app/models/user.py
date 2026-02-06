from app.models.base_model import BaseModel
import re

class User(BaseModel):
    """User entity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_name = (kwargs.get("first_name") or "").strip()
        self.last_name = (kwargs.get("last_name") or "").strip()
        self.email = (kwargs.get("email") or "").strip()
        self.password = kwargs.get("password") or ""
        self.is_admin = bool(kwargs.get("is_admin", False))

    def validate(self):
        """Validate user attributes."""
        # Email validation
        if not self.email:
            return False, "Email is required"
        if not isinstance(self.email, str):
            return False, "Email must be a string"
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            return False, "Invalid email format"
        if len(self.email) > 255:
            return False, "Email must be under 255 characters"
        
        # Password validation
        if not self.password:
            return False, "Password is required"
        if not isinstance(self.password, str):
            return False, "Password must be a string"
        if len(self.password) < 6:
            return False, "Password must be at least 6 characters"
        if len(self.password) > 128:
            return False, "Password must be under 128 characters"
        
        # Name validation (optional fields)
        if self.first_name and len(self.first_name) > 50:
            return False, "First name must be under 50 characters"
        if self.last_name and len(self.last_name) > 50:
            return False, "Last name must be under 50 characters"
        
        return True, None

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "is_admin": self.is_admin,
            }
        )
        return data
