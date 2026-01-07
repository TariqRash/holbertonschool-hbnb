"""HBnB Application Package"""
from app.services.facade import HBnBFacade

# Create a single instance of the facade to be shared across the application
facade = HBnBFacade()
