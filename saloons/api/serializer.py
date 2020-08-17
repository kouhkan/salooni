from rest_framework import serializers
from ..models import Saloon


class SaloonSerializer(serializers.ModelSerializer):

	owner = serializers.SerializerMethodField('get_owner_from_saloon')

	class Meta:
		model = Saloon
		fields = '__all__'
		list(fields).append('owner')

	def get_owner_from_saloon(self, get_saloon):
		owner = get_saloon.owner.username
		return owner
