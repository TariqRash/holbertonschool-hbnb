from typing import Any, List, Optional, Union

from app.models import Amenity, Place, Review, User
from app.persistence.repository import repository


class Facade:
    """Facade to orchestrate business logic and persistence."""

    def __init__(self):
        self.repo = repository

    # Users
    def create_user(
        self,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[User]:
        user = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
        )
        self.repo.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.repo.get(user_id, "User")

    def list_users(self) -> List[User]:
        return self.repo.get_all("User")

    def update_user(
        self,
        user_id: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_admin: Optional[bool] = None,
    ) -> Optional[User]:
        user = self.get_user(user_id)
        if not user:
            return None
        updates: dict[str, Any] = {}
        if email is not None:
            updates["email"] = email
        if password is not None:
            updates["password"] = password
        if first_name is not None:
            updates["first_name"] = first_name
        if last_name is not None:
            updates["last_name"] = last_name
        if is_admin is not None:
            updates["is_admin"] = is_admin
        user.update(**updates)
        self.repo.update(user)
        return user

    # Amenities
    def create_amenity(self, name: str, description: Optional[str] = None) -> Amenity:
        amenity = Amenity(name=name, description=description)
        self.repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        return self.repo.get(amenity_id, "Amenity")

    def list_amenities(self) -> List[Amenity]:
        return self.repo.get_all("Amenity")

    def update_amenity(
        self, amenity_id: str, name: Optional[str] = None, description: Optional[str] = None
    ) -> Optional[Amenity]:
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        updates: dict[str, Any] = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        amenity.update(**updates)
        self.repo.update(amenity)
        return amenity

    # Places
    def _amenities_exist(self, amenity_ids: List[str]) -> bool:
        return all(self.get_amenity(a_id) for a_id in amenity_ids)

    def create_place(
        self,
        title: str,
        description: Optional[str],
        price: float,
        latitude: float,
        longitude: float,
        owner_id: str,
        amenity_ids: Optional[List[str]] = None,
    ) -> Optional[Place]:
        if not owner_id or not self.get_user(owner_id):
            return None
        amenity_ids = amenity_ids or []
        if not self._amenities_exist(amenity_ids):
            return None
        place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner_id=owner_id,
            amenity_ids=amenity_ids,
        )
        self.repo.add(place)
        return place

    def get_place(self, place_id: str) -> Optional[Place]:
        return self.repo.get(place_id, "Place")

    def list_places(self) -> List[Place]:
        return self.repo.get_all("Place")

    def update_place(
        self,
        place_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        owner_id: Optional[str] = None,
        amenity_ids: Optional[List[str]] = None,
    ) -> Optional[Union[Place, bool]]:
        place = self.get_place(place_id)
        if not place:
            return None
        if owner_id is not None and not self.get_user(owner_id):
            return False
        if amenity_ids is not None and not self._amenities_exist(amenity_ids):
            return False
        updates: dict[str, Any] = {}
        if title is not None:
            updates["title"] = title
        if description is not None:
            updates["description"] = description
        if price is not None:
            updates["price"] = price
        if latitude is not None:
            updates["latitude"] = latitude
        if longitude is not None:
            updates["longitude"] = longitude
        if owner_id is not None:
            updates["owner_id"] = owner_id
        if amenity_ids is not None:
            updates["amenity_ids"] = amenity_ids
        place.update(**updates)
        self.repo.update(place)
        return place

    # Reviews
    def create_review(
        self,
        user_id: str,
        place_id: str,
        rating: int,
        text: Optional[str] = None,
    ) -> Optional[Review]:
        if not self.get_user(user_id) or not self.get_place(place_id):
            return None
        review = Review(user_id=user_id, place_id=place_id, rating=rating, text=text)
        self.repo.add(review)
        return review

    def get_review(self, review_id: str) -> Optional[Review]:
        return self.repo.get(review_id, "Review")

    def list_reviews(self) -> List[Review]:
        return self.repo.get_all("Review")

    def list_reviews_for_place(self, place_id: str) -> Optional[List[Review]]:
        if not self.get_place(place_id):
            return None
        return [r for r in self.list_reviews() if r.place_id == place_id]

    def update_review(
        self,
        review_id: str,
        user_id: Optional[str] = None,
        place_id: Optional[str] = None,
        rating: Optional[int] = None,
        text: Optional[str] = None,
    ) -> Optional[Union[Review, bool]]:
        review = self.get_review(review_id)
        if not review:
            return None
        if user_id is not None and not self.get_user(user_id):
            return False
        if place_id is not None and not self.get_place(place_id):
            return False
        updates: dict[str, Any] = {}
        if user_id is not None:
            updates["user_id"] = user_id
        if place_id is not None:
            updates["place_id"] = place_id
        if rating is not None:
            updates["rating"] = rating
        if text is not None:
            updates["text"] = text
        review.update(**updates)
        self.repo.update(review)
        return review

    def delete_review(self, review_id: str) -> bool:
        return self.repo.delete(review_id, "Review")


facade = Facade()
