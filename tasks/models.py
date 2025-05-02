from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    user = models.CharField(max_length=100, unique=True)  # Nombre de usuario único
    password = models.CharField(max_length=128)  # Almacenar contraseñas hasheadas

    class Meta:
        db_table = 'users_login'
        managed = False

    def __str__(self):
        return f"{self.user}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)