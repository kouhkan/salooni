from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import SaloonSerializer
from ..models import Saloon
from accounts.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
# class SaloonView(viewsets.ModelViewSet):
# 	queryset = Saloon.active_saloons.all()
# 	serializer_class = SaloonSerializer
# 	permission_classes = permissions.IsAuthenticatedOrReadOnly


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def api_get_saloon_detail(request, slug):
	try:
		get_saloon = Saloon.objects.get(slug=slug)
	except Saloon.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = SaloonSerializer(get_saloon)
		return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated, ))
def api_change_saloon_detail(request, slug):
	try:
		get_saloon = Saloon.objects.get(slug=slug)
	except Saloon.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if get_saloon.owner != user:
		return Response(data={'status': "You done permission to edit"})

	if request.method == 'PUT':
		serializer = SaloonSerializer(get_saloon, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['status'] = True
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated, ))
def api_delete_saloon_detail(request, slug):
	try:
		get_saloon = Saloon.objects.get(slug=slug)
	except Saloon.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if get_saloon.owner != user:
		return Response(data={'status': "You done permission to delete"})

	if request.method == 'DELETE':
		operation = get_saloon.delete()
		data = {}
		if operation:
			data['status'] = True
		else:
			data['status'] = False
		return Response(data=data)



@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def api_create_saloon_view(request):
	account = request.user
	create_saloon = Saloon(owner=account)

	if request.method == 'POST':
		serializer = SaloonSerializer(create_saloon, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APISaloonListView(ListAPIView):
	queryset = Saloon.active_saloons.all()
	authentication_classes = (TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = SaloonSerializer
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_feilds = ('title', 'city', 'province')