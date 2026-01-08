from app.models.base_model import BaseModel

class User(BaseModel):
    """User entity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_name = kwargs.get("first_name", "").strip()
        self.last_name = kwargs.get("last_name", "").strip()
        self.email = kwargs.get("email", "").strip()
        self.password = kwargs.get("password", "")
        self.is_admin = bool(kwargs.get("is_admin", False))

    def validate(self):
        if not self.email or "@" not in self.email:
            return False, "Valid email is required"
        if not self.password or len(self.password) < 6:
            return False, "Password must be at least 6 characters"
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
