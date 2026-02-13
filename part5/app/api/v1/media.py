"""
HBnB V2 — Media API
Image upload and gallery management.
"""
from flask import request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import api_v1
from app import db
from app.models.media import Media
from app.models.place import Place
import os
import uuid


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_v1.route('/places/<place_id>/media', methods=['GET'])
def place_media(place_id):
    """Get all media for a place"""
    media = Media.query.filter_by(place_id=place_id) \
        .order_by(Media.is_cover.desc(), Media.sort_order).all()

    lang = request.args.get('lang', 'ar')
    return jsonify([m.to_dict(lang) for m in media]), 200


@api_v1.route('/places/<place_id>/media', methods=['POST'])
@jwt_required()
def upload_media(place_id):
    """Upload images for a place — owner only"""
    user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)

    if place.owner_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use: png, jpg, jpeg, webp, gif'}), 400

    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    # Save file
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    # Create media record
    is_cover = request.form.get('is_cover', 'false').lower() == 'true'
    if is_cover:
        # Unset other covers
        Media.query.filter_by(place_id=place_id, is_cover=True).update({'is_cover': False})

    media = Media(
        place_id=place_id,
        url=f"/static/uploads/{filename}",
        caption_en=request.form.get('caption_en', ''),
        caption_ar=request.form.get('caption_ar', ''),
        is_cover=is_cover,
        sort_order=Media.query.filter_by(place_id=place_id).count(),
    )

    db.session.add(media)
    db.session.commit()

    return jsonify({
        'message': 'Image uploaded',
        'message_ar': 'تم رفع الصورة',
        'media': media.to_dict()
    }), 201


@api_v1.route('/media/<media_id>', methods=['DELETE'])
@jwt_required()
def delete_media(media_id):
    """Delete a media item"""
    user_id = get_jwt_identity()
    media = Media.query.get_or_404(media_id)

    place = Place.query.get(media.place_id)
    if not place or place.owner_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Delete file
    try:
        filepath = os.path.join(current_app.root_path, media.url.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass

    db.session.delete(media)
    db.session.commit()

    return jsonify({'message': 'Deleted', 'message_ar': 'تم الحذف'}), 200
