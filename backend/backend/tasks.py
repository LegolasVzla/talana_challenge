from backend.celery import app
from django.core.mail import send_mail

@app.task
def send_email(title, content, to_email):
    send_mail(title, content, 'noreply@mail.com', [to_email], fail_silently=False)