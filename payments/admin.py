from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class Payment(admin.ModelAdmin):
	list_display = ('reserve', 'change_datetime', 'paid', 'status')
	list_filter = ('created', 'paid', 'status')
	list_editable = ('status', 'paid')
	raw_id_fields = ('reserve', )
