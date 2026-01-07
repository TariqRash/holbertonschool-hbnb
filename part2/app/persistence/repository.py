"""In-Memory Repository Implementation"""


class InMemoryRepository:
    """In-memory storage for entities"""

    def __init__(self):
        """Initialize repository with empty storage"""
        self._storage = {}

    def add(self, entity):
        """Add an entity to the repository"""
        self._storage[entity.id] = entity

    def get(self, entity_id):
        """Retrieve an entity by ID"""
        return self._storage.get(entity_id)

    def get_all(self):
        """Retrieve all entities"""
        return list(self._storage.values())

    def update(self, entity_id, data):
        """Update an entity"""
        entity = self.get(entity_id)
        if entity:
            entity.update(data)
            return entity
        return None

    def delete(self, entity_id):
        """Delete an entity"""
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Get entity by a specific attribute value"""
        for entity in self._storage.values():
            if hasattr(entity, attr_name) and getattr(entity, attr_name) == attr_value:
                return entity
        return None
