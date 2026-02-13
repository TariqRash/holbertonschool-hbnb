"""
HBnB V2 — Frontend Routes
Serves HTML pages.
"""
from flask import Blueprint, render_template, request, send_from_directory
import os

frontend = Blueprint('frontend', __name__,
                     template_folder='templates',
                     static_folder='static')


@frontend.route('/')
def index():
    lang = request.args.get('lang', 'ar')
    return render_template('index.html', lang=lang)


@frontend.route('/login')
def login_page():
    lang = request.args.get('lang', 'ar')
    return render_template('login.html', lang=lang)


@frontend.route('/place/<place_id>')
def place_page(place_id):
    lang = request.args.get('lang', 'ar')
    return render_template('place.html', place_id=place_id, lang=lang)


@frontend.route('/booking/<booking_id>')
def booking_page(booking_id):
    lang = request.args.get('lang', 'ar')
    return render_template('booking.html', booking_id=booking_id, lang=lang)


@frontend.route('/bookings')
def bookings_page():
    lang = request.args.get('lang', 'ar')
    return render_template('bookings.html', lang=lang)


@frontend.route('/owner')
def owner_dashboard():
    lang = request.args.get('lang', 'ar')
    return render_template('owner.html', lang=lang)


@frontend.route('/auth/verify')
def verify_magic_link():
    """Magic link verification page"""
    lang = request.args.get('lang', 'ar')
    return render_template('verify.html', lang=lang)


@frontend.route('/search')
def search_page():
    lang = request.args.get('lang', 'ar')
    return render_template('search.html', lang=lang)


# Serve uploads
@frontend.route('/static/uploads/<filename>')
def uploaded_file(filename):
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    return send_from_directory(upload_dir, filename)
