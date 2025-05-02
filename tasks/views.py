from django.shortcuts import render
from django.conf import settings
from .validators import FormValidator
from tasks.models import User
import requests

def register(request):
    errors = {}
    if request.method == 'POST':
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
                user = User(user=username)
                user.set_password(password)
                user.save()
                print("Usuario creado exitosamente")
                messages = "Usuario creado exitosamente"
                return render(request, 'login.html', {'messages': messages, 'site_key': settings.RECAPTCHA_SITE_KEY})
            except Exception as e:
                print("Error al crear el usuario:", str(e))
                errors['user_creation'] = f"Error al crear el usuario: {str(e)}"
        else:
            errors = validator.errors
            print("Errores de validación:", errors)

    return render(request, 'signup.html', {'errors': errors, 'site_key': settings.RECAPTCHA_SITE_KEY})

def login(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        captcha_response = request.POST.get('g-recaptcha-response')

        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': captcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            errors['login'] = "Usuario, contraseña o CAPTCHA incorrectos"
        else:
            try:
                user = User.objects.get(user=username)
                if user.check_password(password):
                    print("Inicio de sesión exitoso")
                    return render(request, 'welcome.html', {})
            except User.DoesNotExist:
                pass

            errors['login'] = "Usuario, contraseña o CAPTCHA incorrectos"

    return render(request, 'login.html', {'errors': errors, 'site_key': settings.RECAPTCHA_SITE_KEY})