from .models import (User)
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('__all__')

	def update(self, instance, data):
		instance.first_name = data.get("first_name")
		instance.last_name = data.get("last_name")
		instance.password = data.get("password")
		instance.save()
		return instance

class CreateUserAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email','first_name','last_name')

class VerifyUserAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email')
