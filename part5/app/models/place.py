"""
HBnB V2 — Place (Property) Model
Supports multiple property types, bilingual, media, privacy radius.
"""
from app import db
from app.models.base_model import BaseModel


# Many-to-many: Place <-> Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class PropertyType(BaseModel):
    """Property type categories"""
    __tablename__ = 'property_types'

    name_en = db.Column(db.String(50), nullable=False, unique=True)
    name_ar = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), nullable=True)  # Lucide icon name
    image_url = db.Column(db.String(500), nullable=True)
    sort_order = db.Column(db.Integer, default=0)

    places = db.relationship('Place', backref='property_type_rel', lazy='dynamic')

    def to_dict(self, lang='ar'):
        return {
            'id': self.id,
            'name': self.name_ar if lang == 'ar' else self.name_en,
            'name_en': self.name_en,
            'name_ar': self.name_ar,
            'icon': self.icon,
            'image_url': self.image_url,
            'place_count': self.places.count() if self.places else 0,
        }


class Place(BaseModel):
    """Property listing — the core model"""
    __tablename__ = 'places'

    # Basic Info
    title_en = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text, nullable=True)
    description_ar = db.Column(db.Text, nullable=True)

    # Pricing
    price_per_night = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='SAR')
    monthly_discount = db.Column(db.Float, default=10.0)  # % discount for 30+ days

    # Location
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False, index=True)
    address = db.Column(db.String(500), nullable=True)  # Only shown post-booking
    latitude = db.Column(db.Float, nullable=True, default=0.0)
    longitude = db.Column(db.Float, nullable=True, default=0.0)

    # Property Details
    property_type_id = db.Column(db.String(36), db.ForeignKey('property_types.id'), nullable=False, index=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)

    # Capacity
    max_guests = db.Column(db.Integer, default=4)
    bedrooms = db.Column(db.Integer, default=1)
    bathrooms = db.Column(db.Integer, default=1)
    beds = db.Column(db.Integer, default=1)

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_instant_book = db.Column(db.Boolean, default=True)

    # Trip type: business, family, both
    trip_type = db.Column(db.String(20), default='both')

    # Access Instructions (only revealed after booking)
    access_instructions_en = db.Column(db.Text, nullable=True)
    access_instructions_ar = db.Column(db.Text, nullable=True)
    floor_number = db.Column(db.String(20), nullable=True)
    door_description_en = db.Column(db.String(200), nullable=True)
    door_description_ar = db.Column(db.String(200), nullable=True)

    # Check-in/out
    check_in_time = db.Column(db.String(10), default='16:00')
    check_out_time = db.Column(db.String(10), default='12:00')

    # House Rules
    rules_en = db.Column(db.Text, nullable=True)
    rules_ar = db.Column(db.Text, nullable=True)

    # Relationships
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places', lazy='subquery')
    media = db.relationship('Media', backref='place', lazy='dynamic', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='place', lazy='dynamic')
    reviews = db.relationship('Review', backref='place', lazy='dynamic')

    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def monthly_price(self):
        """30-day price with discount"""
        daily = self.price_per_night
        total = daily * 30
        discount = total * (self.monthly_discount / 100)
        return round(total - discount, 2)

    def to_dict(self, lang='ar', include_private=False):
        """Convert to dict — private data only shown if user has booked"""
        data = {
            'id': self.id,
            'title': self.title_ar if lang == 'ar' else self.title_en,
            'title_en': self.title_en,
            'title_ar': self.title_ar,
            'description': self.description_ar if lang == 'ar' else self.description_en,
            'price_per_night': self.price_per_night,
            'monthly_price': self.monthly_price,
            'currency': self.currency,
            'city_id': self.city_id,
            'property_type_id': self.property_type_id,
            'max_guests': self.max_guests,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'beds': self.beds,
            'is_featured': self.is_featured,
            'is_instant_book': self.is_instant_book,
            'trip_type': self.trip_type,
            'check_in_time': self.check_in_time,
            'check_out_time': self.check_out_time,
            'average_rating': self.average_rating,
            'review_count': self.review_count,
            'rules': self.rules_ar if lang == 'ar' else self.rules_en,
            'amenities': [a.to_dict(lang) for a in self.amenities],
            'media': [m.to_dict() for m in self.media.all()],
            'owner': self.owner.to_public_dict() if self.owner else None,
            'city': self.city.to_dict(lang) if self.city else None,
            'property_type': self.property_type_rel.to_dict(lang) if self.property_type_rel else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_private:
            # Exact location + access instructions (post-booking only)
            data['latitude'] = self.latitude
            data['longitude'] = self.longitude
            data['address'] = self.address
            data['access_instructions'] = self.access_instructions_ar if lang == 'ar' else self.access_instructions_en
            data['floor_number'] = self.floor_number
            data['door_description'] = self.door_description_ar if lang == 'ar' else self.door_description_en
        else:
            # Privacy radius — approximate location only
            data['latitude'] = round(self.latitude, 1)  # ~11km precision
            data['longitude'] = round(self.longitude, 1)
            data['address'] = None

        return data

    def to_card_dict(self, lang='ar'):
        """Minimal data for listing cards"""
        first_media = self.media.first()
        return {
            'id': self.id,
            'title': self.title_ar if lang == 'ar' else self.title_en,
            'price_per_night': self.price_per_night,
            'monthly_price': self.monthly_price,
            'currency': self.currency,
            'average_rating': self.average_rating,
            'review_count': self.review_count,
            'city': self.city.to_dict(lang) if self.city else None,
            'property_type': self.property_type_rel.to_dict(lang) if self.property_type_rel else None,
            'image_url': first_media.url if first_media else None,
            'is_featured': self.is_featured,
            'max_guests': self.max_guests,
            'bedrooms': self.bedrooms,
        }
