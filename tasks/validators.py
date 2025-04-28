import re

class FormValidator:
    def __init__(self, data):
        self.data = data
        self.errors = {}

    def validate(self):
        username = self.data.get('username', '').strip()
        password1 = self.data.get('password1', '')
        password2 = self.data.get('password2', '')

        # Validar nombre de usuario
        if len(username) < 5:
            self.errors['username'] = "El nombre de usuario debe tener al menos 5 caracteres."

        # Validar contraseña
        if len(password1) < 8:
            self.errors['password1'] = "La contraseña debe tener al menos 8 caracteres."
        if password1 != password2:
            self.errors['password2'] = "Las contraseñas no coinciden."
        if not re.search(r'[A-Za-z]', password1) or not re.search(r'\d', password1):
            self.errors['password1'] = "La contraseña debe contener al menos un carácter alfabético y un número."
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            self.errors['password1'] = "La contraseña debe contener al menos un carácter especial."

        return not bool(self.errors)  # Devuelve True si no hay errores