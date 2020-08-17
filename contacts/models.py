from django.db import models
from khayyam import *


class Contact(models.Model):
	user = models.CharField(max_length=60)
	email = models.EmailField(max_length=100)
	subject = models.CharField(max_length=70)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.BooleanField(default=False)


	def __str__(self):
		return self.user

	def change_datetime(self):
		return JalaliDatetime(self.created)

	class Meta:
		verbose_name = 'تماس'
		verbose_name_plural = 'تماس‌ها'
		ordering = ('-created', )
