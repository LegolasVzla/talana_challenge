from .models import (User)
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('__all__')

class CreateUserAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email','first_name','last_name')

class VerifyUserAccountSerializer(serializers.ModelSerializer):
	#email = serializers.EmailField()
	#user = serializers.IntegerField(source='user_id')
	class Meta:
		model = User
		fields = ('id',)

class GeneratePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)

    def validate(self, data):
        validate_password(data['password'])
        return data
