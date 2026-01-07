"""Base Entity Module - Abstract base class for all entities"""
from datetime import datetime
import uuid
from abc import ABC


class BaseEntity(ABC):
    """Abstract base class for all business entities"""

    def __init__(self):
        """Initialize base entity with ID and timestamps"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update entity attributes"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convert entity to dictionary representation"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
