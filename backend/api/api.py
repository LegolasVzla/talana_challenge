import os
import json
import logging
import random
from datetime import datetime
from functools import wraps

from api.models import (User)
from api.serializers import (UserSerializer,CreateUserAccountSerializer,
	VerifyUserAccountSerializer)
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import (viewsets, permissions,views,status,serializers,
	exceptions)
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.settings import BASE_DIR 
from backend.tasks import send_email

User = get_user_model()

def validate_type_of_request(f):
	'''
	Allows to validate the type of request for the endpoints
	'''
	@wraps(f)
	def decorator(*args, **kwargs):
		if(len(kwargs) > 0):
			# HTML template
			kwargs['data'] = kwargs
		# DRF raw data, HTML form input
		elif len(args[1].data) > 0:
			kwargs['data'] = args[1].data
		# Postman POST request made by params
		elif len(args[1].query_params.dict()) > 0:
			kwargs['data'] = args[1].query_params.dict()
		return f(*args,**kwargs)
	return decorator

class UserViewSet(viewsets.ModelViewSet):
	'''
	Class related with the User Model.
	'''
	queryset = User.objects.filter(
		is_active=True,
		is_deleted=False
	).order_by('id')
	permission_classes = [
		permissions.AllowAny
	]

	def __init__(self,*args, **kwargs):
		self.response_data = {'error': [], 'data': []}
		self.data = {}
		self.code = status.HTTP_200_OK		

	def get_serializer_class(self):
		if self.action in ['create_account']:
			return CreateUserAccountSerializer
		if self.action in ['verify_account']:
			import pdb;pdb.set_trace()
			return VerifyUserAccountSerializer			
		return UserSerializer

	@validate_type_of_request
	@action(methods=['post'], detail=False)	
	def create_account(self, request, *args, **kwargs):
		'''This method allows to create a new account'''
		try:
			serializer = CreateUserAccountSerializer(data=kwargs['data'])
			if serializer.is_valid():
				serializer.save()
				self.response_data['data'].append(serializer.data)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - UserView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)

	@validate_type_of_request
	@action(methods=['post'], detail=False)	
	def verify_account(self, request, *args, **kwargs):
		'''This method allows to verify a new account'''
		try:
			serializer = VerifyUserAccountSerializer(data=kwargs['data'])
			if serializer.is_valid():
				instance = User.objects.get(email=kwargs['data']['email'])
				instance.is_active = True
				serializer.save()
				self.response_data['data'].append({'message':'Your account has been verified'})
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
			self.response_data['error'].append("[API - UserView] - Error: " + str(e))
		return Response(self.response_data,status=self.code)