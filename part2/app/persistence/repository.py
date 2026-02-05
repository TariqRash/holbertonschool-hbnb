import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

class Repository:
    """Simple in-memory repository."""

    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}

    def _bucket(self, entity_type: str) -> Dict[str, Any]:
        if entity_type not in self._storage:
            self._storage[entity_type] = {}
        return self._storage[entity_type]

    def add(self, entity) -> None:
        if not getattr(entity, "id", None):
            entity.id = str(uuid.uuid4())
        if not getattr(entity, "created_at", None):
            entity.created_at = datetime.utcnow()
        bucket = self._bucket(entity.__class__.__name__)
        bucket[entity.id] = entity

    def get(self, entity_id: str, entity_type: str) -> Optional[Any]:
        return self._bucket(entity_type).get(entity_id)

    def get_all(self, entity_type: str) -> List[Any]:
        return list(self._bucket(entity_type).values())

    def update(self, entity) -> None:
        entity_type = entity.__class__.__name__
        bucket = self._bucket(entity_type)
        bucket[entity.id] = entity

    def delete(self, entity_id: str, entity_type: str) -> bool:
        bucket = self._bucket(entity_type)
        if entity_id in bucket:
            del bucket[entity_id]
            return True
        return False

    def exists(self, entity_id: str, entity_type: str) -> bool:
        return entity_id in self._bucket(entity_type)

repository = Repository()
