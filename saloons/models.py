from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from taggit.managers import TaggableManager
from khayyam import *
from .managers import ActiveSaloonManager
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache


class Feature(models.Model):
	name = models.CharField(max_length=70, verbose_name='نام')
	slug = models.SlugField(max_length=70, verbose_name='اسلاگ')
	created = models.DateTimeField(auto_now_add=True, verbose_name='زمان افزودن')
	updated = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True, verbose_name='وضعیت')


	def __str__(self):
		return self.name

	class Meta:
		ordering = ('-created', )
		verbose_name = 'امکان'
		verbose_name_plural = 'امکانات'

	def change_datetime(self):
		return JalaliDatetime(self.created)

	change_datetime.short_description = 'زمان افزودن'


class Saloon(models.Model):
	STATUS = (
		('a', 'فعال'),
		('d', 'غیرفعال'),
	)
	GENDER = (
		('m', 'آقایان'),
		('f', 'بانوان'),
		('b', 'آقایان و بانوان'),
	)
	TYPE = (
		('su', 'چمن'),
		('sa', 'سالن'),
	)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL,
	                          on_delete=models.CASCADE,
	                          related_name='owner',
	                          verbose_name='مالک')
	name = models.CharField(max_length=100, verbose_name='نام سالن')
	slug = models.SlugField(max_length=100,
	                        unique=True,
	                        verbose_name='اسلاگ',
	                        allow_unicode=True)
	picture = models.ImageField(upload_to=f'saloons/%Y/%m/%d/',
	                            verbose_name='انتخاب تصویر')
	about = RichTextUploadingField(verbose_name='درباره سالن')
	tags = TaggableManager(verbose_name='رشته‌های سالن')
	area = models.CharField(max_length=50, verbose_name='فضای سالن')
	features = models.ManyToManyField(Feature,
	                                  related_name='features',
	                                  verbose_name='امکانات سالن',
	                                  blank=True)
	start_time = models.PositiveIntegerField(verbose_name='ساعت شروع')
	end_time = models.PositiveIntegerField(verbose_name='ساعت پایان')
	amount = models.PositiveIntegerField(verbose_name='هزینه هر سانس')
	on_map = models.CharField(max_length=100, null=True, blank=True, verbose_name='موقعیت نقشه')
	province = models.CharField(max_length=50, verbose_name='استان')
	city = models.CharField(max_length=100, verbose_name='شهر')
	address = models.TextField(verbose_name='آدرس')
	created = models.DateTimeField(auto_now_add=True, verbose_name='زمان افزودن')
	updated = models.DateTimeField(auto_now=True)
	type = models.CharField(max_length=2, choices=TYPE, default='su', verbose_name='نوع')
	gender = models.CharField(max_length=1, choices=GENDER, default='b', verbose_name='مخصوص')
	status = models.CharField(max_length=1, choices=STATUS, default='d', verbose_name='وضعیت سالن')

	objects = models.Manager()
	active_saloons = ActiveSaloonManager()


	def get_absoulte_url(self):
		return reverse('saloons:saloons_detail', kwargs={'slug': self.slug})


	def __str__(self):
		return f'{self.owner} - {self.name}'

	class Meta:
		ordering = ('-created', )
		verbose_name = 'سالن'
		verbose_name_plural = 'سالن‌ها'

	def change_datetime(self):
		return JalaliDatetime(self.created)
	change_datetime.short_description = 'زمان افزودن'


@receiver(post_save, sender=Saloon)
def clear_cache(sender, instance, **kwargs):
	cache.clear()


class Image(models.Model):
	saloon = models.ForeignKey(Saloon,
	                           on_delete=models.CASCADE,
	                           related_name='saloon_image',
	                           verbose_name='انتخاب سالن')
	picture = models.ImageField(upload_to=f'saloons/%Y/%m/%d/',
	                            verbose_name='انتخاب تصویر')
	created = models.DateTimeField(auto_now_add=True, verbose_name='زمان افزودن')
	updated = models.DateTimeField(auto_now=True)
	status = models.BooleanField(default=True, verbose_name='وضعیت')


	def __str__(self):
		return f'{self.saloon}'

	class Meta:
		ordering = ('-created', )
		verbose_name = 'تصویر'
		verbose_name_plural = 'تصاویر'

	def change_datetime(self):
		return JalaliDatetime(self.created)
	change_datetime.short_description = 'زمان افزودن'