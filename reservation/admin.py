from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
	list_display = ('user', 'saloon', 'change_datetime', 'hour',  'status')
	list_filter = ('user', 'saloon', 'status')
	search_fields = ('user', 'saloon')
	list_editable = ('status', )
	raw_id_fields = ('user', 'saloon')