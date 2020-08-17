from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response
from rest_framework.authtoken.models import Token

from .serializers import (RegistrationSerializer,
                          AccountPropertiesSerializer,
                          LoginSerializer)
from ..models import User
from django.contrib.auth import authenticate


@api_view(['POST'])
def api_register_view(request):
	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registerd a new user'
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors

		return Response(data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def api_account_login_view(request):

	if request.method == 'POST':
		serializer = LoginSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			print('&'*100, 'is_valid')
			check_auth = authenticate(request,
			                          username=serializer.data.get('username'),
			                          password=serializer.data.get('password'))
			if check_auth:
				token = Token.objects.get(user__username=serializer.data.get('username'))

				data['response'] = 'Login is successful.'
				data['token'] = token
				return Response(data=data)
			else:
				data['response'] = 'Authentication is failed.'
				return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_account_detail_view(request):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = AccountPropertiesSerializer(account)
		return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def api_account_detail_update_view(request):
	try:
		account = request.user
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'PUT':
		serializer = AccountPropertiesSerializer(account, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = "Account is updated."
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

