from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'


urlpatterns = [
	path('register/', views.api_register_view, name='api_register'),
	path('login/', views.api_account_login_view, name='api_login'),
	path('properties/', views.api_account_detail_view, name='api_properties'),
	path('properties/update/', views.api_account_detail_update_view, name='api_properties_update'),
	path('login/', obtain_auth_token, name='api_login'),
]