from django.shortcuts import render
from apps.base.utilits import send_mail_code

def index(request):

    return render(request, 'home.html')