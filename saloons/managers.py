from django.db import models


class ActiveSaloonManager(models.Manager):
	def get_queryset(self):
		return super(ActiveSaloonManager, self).get_queryset().filter(status='a')