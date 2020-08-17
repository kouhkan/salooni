from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('user', 'email', 'subject', 'change_datetime')
	list_filter = ('created', )
	search_fields = ('email', 'user', 'subject')