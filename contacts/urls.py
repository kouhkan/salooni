from django.urls import path
from . import views

app_name = 'contacts'


urlpatterns = [
	path('us/', views.contact, name='contact'),
	path('about-us/', views.about, name='about'),
]