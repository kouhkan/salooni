from django.urls import path, include
from . import views


app_name = 'saloons'

urlpatterns = [
	path('api/v1/', include('saloons.api.urls', namespace='saloons')),
	path('', views.saloon_list, name='saloons_list'),
	path('<slug:slug>/', views.saloon_detail, name='saloons_detail'),
	path('city/<str:slug>/', views.saloon_city, name='saloons_city'),
	# path('search-city/', views.search_city, name='search_city'),
	path('province/<str:slug>/', views.saloon_province, name='saloons_province'),
	path('payment/<int:reserve_id>/<int:amount>/', views.payment, name='payment'),
	path('payment/verify/', views.verify, name='verify'),
]