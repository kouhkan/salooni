from django.db import models
from accounts.models import User
from saloons.models import Saloon
from khayyam import *


class Reservation(models.Model):
	STATUS = (
		('t', 'موقت'),
		('r', 'رزرو شده'),
	)
	user = models.ForeignKey(User,
	                         on_delete=models.CASCADE,
	                         related_name='user_reservation')
	saloon = models.ForeignKey(Saloon,
	                           on_delete=models.CASCADE,
	                           related_name='saloon_reservation')
	reserve_date = models.DateField()
	hour = models.PositiveIntegerField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=1, default='t', choices=STATUS)


	def change_datetime(self):
		return JalaliDate(self.reserve_date).strftime('%Y-%m-%d')

	def __str__(self):
		return f'{self.user} reserved {self.saloon} at {self.reserve_date}'

	class Meta:
		ordering = ('-created', )
		verbose_name = 'رزرو'
		verbose_name_plural = 'رزرو شده‌ها'


# datetime.strptime(x, '%Y/%m/%d %H')
# JalaliDatetime(y)
