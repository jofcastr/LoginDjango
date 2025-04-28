from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from .validators import FormValidator
import requests

def register(request):
    errors = {}
    if request.method == 'POST':
        print("prueba: ", request.POST)
        validator = FormValidator(request.POST)
        
        captcha_response = request.POST.get('g-recaptcha-response')
        
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': captcha_response
        }
        
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        
        if not result.get('success'):
            errors['captcha'] = 'Verificación CAPTCHA fallida. Inténtalo de nuevo.'
        elif validator.validate():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                print("Usuario creado exitosamente")
                return render(request, 'login.html', {'errors': errors, 'site_key': settings.RECAPTCHA_SITE_KEY})
            except Exception as e:
                errors['user_creation'] = f"Error al crear el usuario: {str(e)}"
        else:
            errors = validator.errors
            print("Errores de validación:", errors)

    return render(request, 'signup.html', {'errors': errors, 'site_key': settings.RECAPTCHA_SITE_KEY})

def login(request):
    if request.method == 'POST':
        return render(request, 'welcome.html', {})
    else:
        return render(request, 'login.html', {})