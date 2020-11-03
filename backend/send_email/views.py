from django.shortcuts import render, HttpResponse
from backend.tasks import send_email

# Create your views here.
def index(request):
	send_email.delay("Asunto", "Contenido mensaje", "mail@mail.com")
	return HttpResponse("Enviado")