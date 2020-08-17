from django.contrib import admin
from .models import Saloon, Feature, Image


@admin.register(Saloon)
class SaloonAdmin(admin.ModelAdmin):
	list_display = ('owner', 'name', 'province', 'city', 'change_datetime', 'status')
	list_filter = ('city', 'province', 'created')
	search_fields = ('name', 'owner', 'about')
	raw_id_fields = ('owner', )
	prepopulated_fields = {'slug': ('name', )}
	list_editable = ('status', )
	list_per_page = 20


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
	list_display = ('name', 'change_datetime', 'is_active')
	list_filter = ('is_active', 'created')
	search_fields = ('name', )
	prepopulated_fields = {'slug': ('name', )}
	list_editable = ('is_active', )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display = ('saloon', 'change_datetime', 'status')
	list_filter = ('created', 'status')
	search_fields = ('saloon', )
	list_per_page = 30