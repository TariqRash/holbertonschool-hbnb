# SQLAlchemyRepository for generic CRUD operations
from app import db


class SQLAlchemyRepository:
    """Generic SQLAlchemy repository for CRUD operations"""
    
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add a new object to the database"""
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Get object by ID"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Get all objects of this type"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object by ID"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete an object by ID"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Get object by a single attribute"""
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
        ).first()

    def get_by_attributes(self, **kwargs):
        """Get object by multiple attributes"""
        return self.model.query.filter_by(**kwargs).first()
