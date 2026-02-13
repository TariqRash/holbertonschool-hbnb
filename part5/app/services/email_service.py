"""
HBnB V2 — Email Service
Sends OTP codes and Magic Links via Resend.
https://resend.com/docs/send-with-python
"""
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def _send_email(to, subject, html):
    """Send an email using Resend SDK"""
    api_key = current_app.config.get('RESEND_API_KEY')
    from_email = current_app.config.get('RESEND_FROM_EMAIL', 'noreply@hbnb.sa')

    if not api_key:
        logger.warning(f"[EMAIL DEMO] To: {to} | Subject: {subject}")
        logger.warning(f"[EMAIL DEMO] Body: {html[:200]}...")
        print(f"\n📧 [DEMO EMAIL] To: {to}")
        print(f"   Subject: {subject}")
        print(f"   Body preview: {html[:150]}...\n")
        return True

    try:
        import resend
        resend.api_key = api_key

        params = {
            "from": from_email,
            "to": [to],
            "subject": subject,
            "html": html,
        }

        email = resend.Emails.send(params)
        logger.info(f"Email sent to {to}: {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")
        return False


def send_otp_email(email, code):
    """Send OTP verification code"""
    subject = f"رمز التحقق - HBnB | Your verification code"

    html = f"""
    <div dir="rtl" style="font-family: 'Cairo', Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 30px; background: #fff; border-radius: 12px; border: 1px solid #e5e7eb;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #1a1a2e; font-size: 24px;">🏠 HBnB</h1>
        </div>

        <h2 style="color: #333; text-align: center;">رمز التحقق الخاص بك</h2>
        <p style="color: #666; text-align: center;">Your verification code</p>

        <div style="text-align: center; margin: 30px 0;">
            <div style="display: inline-block; padding: 20px 40px; background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; font-size: 36px; font-weight: bold; letter-spacing: 8px; border-radius: 12px;">
                {code}
            </div>
        </div>

        <p style="color: #888; text-align: center; font-size: 14px;">
            ينتهي هذا الرمز خلال 10 دقائق<br>
            This code expires in 10 minutes
        </p>

        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">

        <p style="color: #aaa; text-align: center; font-size: 12px;">
            إذا لم تطلب هذا الرمز، تجاهل هذه الرسالة<br>
            If you didn't request this code, please ignore this email
        </p>
    </div>
    """

    return _send_email(email, subject, html)


def send_magic_link_email(email, magic_url):
    """Send magic link for passwordless login"""
    subject = f"رابط الدخول - HBnB | Login Link"

    html = f"""
    <div dir="rtl" style="font-family: 'Cairo', Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 30px; background: #fff; border-radius: 12px; border: 1px solid #e5e7eb;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #1a1a2e; font-size: 24px;">🏠 HBnB</h1>
        </div>

        <h2 style="color: #333; text-align: center;">رابط الدخول السحري</h2>
        <p style="color: #666; text-align: center;">Your magic login link</p>

        <div style="text-align: center; margin: 30px 0;">
            <a href="{magic_url}"
               style="display: inline-block; padding: 16px 40px; background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; font-size: 18px; font-weight: bold; text-decoration: none; border-radius: 12px;">
                🔑 تسجيل الدخول — Login
            </a>
        </div>

        <p style="color: #888; text-align: center; font-size: 14px;">
            ينتهي هذا الرابط خلال 30 دقيقة<br>
            This link expires in 30 minutes
        </p>

        <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; margin-top: 20px;">
            <p style="color: #888; font-size: 12px; word-break: break-all; direction: ltr; text-align: left;">
                {magic_url}
            </p>
        </div>

        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">

        <p style="color: #aaa; text-align: center; font-size: 12px;">
            إذا لم تطلب هذا الرابط، تجاهل هذه الرسالة<br>
            If you didn't request this link, please ignore this email
        </p>
    </div>
    """

    return _send_email(email, subject, html)


def send_booking_confirmation(email, booking_data):
    """Send booking confirmation receipt"""
    subject = f"تأكيد الحجز - HBnB | Booking Confirmation"

    html = f"""
    <div dir="rtl" style="font-family: 'Cairo', Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 30px; background: #fff; border-radius: 12px; border: 1px solid #e5e7eb;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #1a1a2e; font-size: 24px;">🏠 HBnB</h1>
        </div>

        <h2 style="color: #16a34a; text-align: center;">✅ تم تأكيد الحجز</h2>
        <p style="color: #666; text-align: center;">Booking Confirmed</p>

        <div style="background: #f0fdf4; padding: 20px; border-radius: 12px; margin: 20px 0;">
            <p><strong>العقار:</strong> {booking_data.get('place_title', '')}</p>
            <p><strong>تاريخ الوصول:</strong> {booking_data.get('check_in', '')}</p>
            <p><strong>تاريخ المغادرة:</strong> {booking_data.get('check_out', '')}</p>
            <p><strong>عدد الليالي:</strong> {booking_data.get('nights', '')}</p>
            <p><strong>المبلغ الإجمالي:</strong> {booking_data.get('total', '')} {booking_data.get('currency', 'SAR')}</p>
        </div>

        <p style="color: #888; text-align: center; font-size: 14px;">
            ستحصل على تفاصيل الوصول قبل موعد الحجز<br>
            You'll receive access details before your check-in date
        </p>
    </div>
    """

    return _send_email(email, subject, html)
