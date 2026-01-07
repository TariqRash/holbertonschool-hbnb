"""API Layer Package"""
from flask_restx import Api

api = Api(
    version='1.0',
    title='HBnB API',
    description='HBnB Application API',
    doc='/api/v1/docs'
)

# Import namespaces after api is created to avoid circular imports
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns

api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(places_ns, path='/api/v1/places')
api.add_namespace(reviews_ns, path='/api/v1/reviews')
api.add_namespace(amenities_ns, path='/api/v1/amenities')
