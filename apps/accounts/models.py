import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from apps.base.models import BaseModel

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', default='default/user.png ', blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self):
        return f"{self.first_name} + {self.last_name}"


    def save(self, *args, **kwargs):
        if self.username:
            self.phone = self.username
            super().save(*args, **kwargs)



    def __str__(self):
        return self.username


EMAIL_EXPIRE_TIME = 5

class UserResetPassword(BaseModel):
    private_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=True, null=True, unique=False)
    code = models.CharField(max_length=15, blank=True, null=True)
    expiration_time = models.DateTimeField(blank=True, null=True)
    is_confirmation = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.email} - {self.code}"


    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE_TIME)
        return super(UserResetPassword, self).save(*args, **kwargs)