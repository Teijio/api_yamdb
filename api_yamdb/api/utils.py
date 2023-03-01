import random

from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_YAMDB


def generate_confirmation_code():
    return int("".join([str(random.randint(0, 10)) for _ in range(6)]))


def send_confirmation_code(email, confirmation_code):
    send_mail(
        subject="Код подтверждения",
        message=f"Код подтверждения: {confirmation_code}",
        from_email=EMAIL_YAMDB,
        recipient_list=(email,),
        fail_silently=False,
    )
