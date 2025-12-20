from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = user.pk

    verification_link = (
        f"http://localhost:8000/api/auth/verify/{uid}/{token}/"
    )

    subject = "Verify your email address"
    message = (
        f"Hi {user.username},\n\n"
        f"Please verify your email by clicking the link below:\n"
        f"{verification_link}\n\n"
        f"Thank you!"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
