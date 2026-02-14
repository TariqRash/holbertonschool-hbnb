"""
HBnB V2 — Auth API
OTP login, Magic Link login, Owner registration, Password login (fallback)
"""
from flask import request, jsonify, current_app, url_for
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from app.api.v1 import api_v1
from app import db
from app.models.user import User
from app.models.otp import OTP
from app.services.email_service import send_otp_email, send_magic_link_email
from datetime import datetime, timedelta, timezone


# ─── Request OTP ────────────────────────────────────────────
@api_v1.route('/auth/otp/request', methods=['POST'])
def request_otp():
    """Send OTP code to email"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'error': 'Email is required', 'error_ar': 'البريد الإلكتروني مطلوب'}), 400

    # Invalidate previous OTPs
    OTP.query.filter_by(email=email, is_used=False, token_type='otp').update({'is_used': True})

    # Generate new OTP
    code = OTP.generate_otp(current_app.config.get('OTP_LENGTH', 6))
    expiry = current_app.config.get('OTP_EXPIRY_MINUTES', 10)

    otp = OTP(
        email=email,
        code=code,
        token_type='otp',
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=expiry)
    )
    db.session.add(otp)
    db.session.commit()

    # Send email
    send_otp_email(email, code)

    return jsonify({
        'message': 'OTP sent successfully',
        'message_ar': 'تم إرسال رمز التحقق بنجاح',
        'expires_in': expiry * 60
    }), 200


# ─── Verify OTP ─────────────────────────────────────────────
@api_v1.route('/auth/otp/verify', methods=['POST'])
def verify_otp():
    """Verify OTP code and login/register user"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    code = data.get('code', '').strip()

    if not email or not code:
        return jsonify({'error': 'Email and code are required'}), 400

    # Find valid OTP
    otp = OTP.query.filter_by(
        email=email, code=code, token_type='otp', is_used=False
    ).order_by(OTP.created_at.desc()).first()

    if not otp or not otp.is_valid:
        if otp:
            otp.attempts += 1
            db.session.commit()
        return jsonify({
            'error': 'Invalid or expired OTP',
            'error_ar': 'رمز التحقق غير صالح أو منتهي الصلاحية'
        }), 401

    # Mark OTP as used
    otp.is_used = True
    db.session.commit()

    # Find or create user
    user = User.query.filter_by(email=email).first()
    is_new = False

    if not user:
        # Auto-register
        user = User(
            first_name=data.get('first_name', email.split('@')[0]),
            last_name=data.get('last_name', ''),
            email=email,
            is_verified=True,
            role='guest',
            preferred_language=data.get('language', 'ar')
        )
        db.session.add(user)
        db.session.commit()
        is_new = True
    else:
        user.is_verified = True
        db.session.commit()

    # Generate tokens
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role, 'email': user.email}
    )
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'message': 'Login successful',
        'message_ar': 'تم تسجيل الدخول بنجاح',
        'is_new_user': is_new,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(include_private=True)
    }), 200


# ─── Request Magic Link ─────────────────────────────────────
@api_v1.route('/auth/magic-link/request', methods=['POST'])
def request_magic_link():
    """Send magic link to email"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Invalidate previous tokens
    OTP.query.filter_by(email=email, is_used=False, token_type='magic_link').update({'is_used': True})

    # Generate token
    token = OTP.generate_magic_token()
    expiry = current_app.config.get('MAGIC_LINK_EXPIRY_MINUTES', 30)

    otp = OTP(
        email=email,
        code=token,
        token_type='magic_link',
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=expiry)
    )
    db.session.add(otp)
    db.session.commit()

    # Send email with magic link
    base_url = request.host_url.rstrip('/')
    magic_url = f"{base_url}/auth/verify?token={token}&email={email}"
    send_magic_link_email(email, magic_url)

    return jsonify({
        'message': 'Magic link sent',
        'message_ar': 'تم إرسال رابط الدخول السحري',
        'expires_in': expiry * 60
    }), 200


# ─── Verify Magic Link ──────────────────────────────────────
@api_v1.route('/auth/magic-link/verify', methods=['POST'])
def verify_magic_link():
    """Verify magic link token"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    token = data.get('token', '').strip()

    if not email or not token:
        return jsonify({'error': 'Email and token required'}), 400

    otp = OTP.query.filter_by(
        email=email, code=token, token_type='magic_link', is_used=False
    ).first()

    if not otp or not otp.is_valid:
        return jsonify({'error': 'Invalid or expired link', 'error_ar': 'الرابط غير صالح أو منتهي'}), 401

    otp.is_used = True
    db.session.commit()

    # Find or create user
    user = User.query.filter_by(email=email).first()
    is_new = False

    if not user:
        user = User(
            first_name=email.split('@')[0],
            last_name='',
            email=email,
            is_verified=True,
            role='guest',
            preferred_language='ar'
        )
        db.session.add(user)
        db.session.commit()
        is_new = True
    else:
        user.is_verified = True
        db.session.commit()

    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role, 'email': user.email}
    )
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'message': 'Login successful',
        'message_ar': 'تم تسجيل الدخول بنجاح',
        'is_new_user': is_new,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(include_private=True)
    }), 200


# ─── Password Login (Fallback) ──────────────────────────────
@api_v1.route('/auth/login', methods=['POST'])
def login():
    """Traditional email/password login"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({
            'error': 'Invalid credentials',
            'error_ar': 'بيانات الدخول غير صحيحة'
        }), 401

    if not user.is_active:
        return jsonify({'error': 'Account disabled', 'error_ar': 'الحساب معطل'}), 403

    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role, 'email': user.email}
    )
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(include_private=True)
    }), 200


# ─── Owner Registration ─────────────────────────────────────
@api_v1.route('/auth/register/owner', methods=['POST'])
def register_owner():
    """Register as property owner — auto-login with JWT"""
    data = request.get_json()

    required = ['first_name', 'last_name', 'email', 'phone', 'password']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required',
                           'error_ar': 'جميع الحقول مطلوبة'}), 400

    email = data['email'].strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered', 'error_ar': 'البريد مسجل مسبقاً'}), 409

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=email,
        phone=data.get('phone'),
        role='owner',
        is_verified=True,
        preferred_language=data.get('language', 'ar')
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    # Auto-login — return JWT tokens immediately
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role, 'email': user.email}
    )
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'message': 'Owner registered successfully',
        'message_ar': 'تم تسجيل المالك بنجاح',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(include_private=True)
    }), 201


# ─── Refresh Token ───────────────────────────────────────────
@api_v1.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_active:
        return jsonify({'error': 'Invalid user'}), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role, 'email': user.email}
    )

    return jsonify({'access_token': access_token}), 200


# ─── Get Current User ───────────────────────────────────────
@api_v1.route('/auth/me', methods=['GET'])
@jwt_required()
def get_me():
    """Get current authenticated user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict(include_private=True)), 200


# ─── Update Profile ─────────────────────────────────────────
@api_v1.route('/auth/me', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    allowed = ['first_name', 'last_name', 'phone', 'bio', 'avatar_url', 'preferred_language', 'sex']

    for field in allowed:
        if field in data:
            setattr(user, field, data[field])

    db.session.commit()

    return jsonify({
        'message': 'Profile updated',
        'message_ar': 'تم تحديث الملف الشخصي',
        'user': user.to_dict(include_private=True)
    }), 200
