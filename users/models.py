import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

CITY_CHOICES = [
    ('Moscow', 'Moscow'),
    ('Saint Petersburg', 'Saint Petersburg'),
    ('Novosibirsk', 'Novosibirsk'),
    ('Kazan', 'Kazan'),
    ('Krasnoyarsk', 'Krasnoyarsk'),
    ('Yekaterinburg', 'Yekaterinburg'),
    ('Omsk', 'Omsk'),
    ('Tomsk', 'Tomsk'),

]


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone_number = PhoneNumberField(max_length=35, verbose_name="phone number", blank=True, null=True)
    tg_name = models.CharField(max_length=50, verbose_name="tg name", blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="avatar", blank=True, null=True)
    city = models.CharField(max_length=50, choices=CITY_CHOICES, verbose_name="city", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="is active", default=False)
    verification_token = models.CharField(max_length=50, blank=True, null=True, verbose_name="Verification Token")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.verification_token:
            self.verification_token = self.generate_verification_token()
        super().save(*args, **kwargs)

    def generate_verification_token(self):
        return str(uuid.uuid4())
