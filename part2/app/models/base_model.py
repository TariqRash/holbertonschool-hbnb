import uuid
from datetime import datetime

class BaseModel:
    """Base model with id and timestamps."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at", datetime.utcnow())
        self.updated_at = kwargs.get("updated_at", datetime.utcnow())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }

    def touch(self):
        self.updated_at = datetime.utcnow()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key not in {"id", "created_at"}:
                setattr(self, key, value)
        self.touch()
