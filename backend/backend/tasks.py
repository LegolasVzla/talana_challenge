from backend.celery import app
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from backend.settings import EMAIL_HOST_USER,EMAIL_HOST
# from django.core.mail import send_mail

'''
def send_email(subject, content, to_email):
    send_mail(subject, content, 'noreply@mail.com', [to_email], fail_silently=False)
'''

@app.task
def send_email(subject,to_email,user,user_id,template_file,message_description):
	html_template = get_template('emails/'+template_file+'.html')
	context = {'email': to_email, 'user': user, 'user_id': user_id}
	html_content = html_template.render(context)
	from_email = EMAIL_HOST_USER
	email = EmailMultiAlternatives(subject,message_description,from_email,[to_email])
	email.attach_alternative(html_content,'text/html')
	email.send()