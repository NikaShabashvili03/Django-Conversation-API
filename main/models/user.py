from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from ..utils import image_upload, validate_image


def upload_avatar(instance, filename):
    return image_upload(instance, filename, 'message/')


class User(AbstractBaseUser):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to=upload_avatar, null=True, blank=True)
    email = models.EmailField(unique=True)

    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def clean(self):
        if self.avatar:
            validate_image(self.avatar, 4000, 4000, 4000)

    def save(self, *args, **kwargs):
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()
        if self.pk is None: 
            self.set_password(self.password) 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.email}"