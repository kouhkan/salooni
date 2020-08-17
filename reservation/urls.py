from django.urls import path
from . import views


app_name = 'reserve'

urlpatterns = [
	path('create/', views.create_reserve, name='create_reserve'),
]