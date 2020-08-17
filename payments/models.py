from django.db import models
from reservation.models import Reservation
from khayyam import *


class Payment(models.Model):
	reserve = models.ForeignKey(Reservation,
	                            on_delete=models.CASCADE,
	                            related_name='reserve_payments')
	refid = models.IntegerField()
	authority = models.CharField(max_length=40)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)
	status = models.IntegerField()

	def __str__(self):
		return f'{self.reserve}'

	def change_datetime(self):
		return JalaliDatetime(self.created).strftime('%Y-%m-%d %H:%M')

	class Meta:
		ordering = ('-created', )
		verbose_name = 'پرداخت'
		verbose_name_plural = 'پرداختی‌ها'