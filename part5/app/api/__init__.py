"""
HBnB V2 — API v1 Blueprint
"""
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)

from app.api.v1 import auth, places, bookings, payments, reviews, amenities, media, cities, maps, users
