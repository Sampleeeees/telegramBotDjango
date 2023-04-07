from django.db import models
from django.utils.html import mark_safe


# Create your models here.

class TelegramUser(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Імя', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Прізвище', blank=True, null=True)
    username = models.CharField(max_length=40, verbose_name="Username", null=True, blank=True, default='None')
    password = models.CharField(max_length=255, blank=True, null=True)
    photo = models.BinaryField(null=True, blank=True)


    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user
        self.save()

    def get_username(self):
        return mark_safe(f"<a href='https://t.me/{self.username}'>@{self.username}</a>")