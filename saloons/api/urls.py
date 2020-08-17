from django.urls import path
from . import views


app_name = 'saloons'

urlpatterns = [
	path('saloon/<slug:slug>/', views.api_get_saloon_detail, name='api_saloon_detail'),
	path('saloon/<slug:slug>/update/', views.api_change_saloon_detail, name='api_saloon_update'),
	path('saloon/<slug:slug>/delete/', views.api_delete_saloon_detail, name='api_saloon_delete'),
	path('saloon/create/', views.api_create_saloon_view, name='api_saloon_create'),
	path('saloon/list', views.APISaloonListView.as_view(), name='api_saloon_list'),
]