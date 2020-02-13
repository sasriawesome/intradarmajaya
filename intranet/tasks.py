import dramatiq
from django.core.mail import send_mail
from django.utils.html import strip_tags

@dramatiq.actor
def send_html_email(subject, from_email, recipient_list, message):
    send_mail(
        subject=subject,
        message=strip_tags(message),
        recipient_list=recipient_list,
        from_email=from_email,
        html_message=message
    )
