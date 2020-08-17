from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MyUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
	username = models.CharField(max_length=25, primary_key=True, verbose_name='نام کاربری')
	email = models.EmailField(max_length=100, unique=True, verbose_name='پست الکترونیکی')
	phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره موبایل')
	is_active = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = MyUserManager()

	def __str__(self):
		return str(self.username)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
	avatar = models.ImageField(upload_to='users/avatars/%Y/%m/', null=True, blank=True, verbose_name='آواتار')
	city = models.CharField(max_length=150, null=True, blank=True, verbose_name='شهر')
	province = models.CharField(max_length=150, null=True, blank=True, verbose_name='استان')


	def __str__(self):
		return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)