import os
import json
import logging
import random
from datetime import datetime
from functools import wraps

from api.models import (User)
from api.serializers import (
    UserSerializer,
    CreateUserAccountSerializer,
    VerifyUserAccountSerializer,
    GeneratePasswordSerializer)
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import (viewsets, permissions, views, status, serializers,
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
        return f(*args, **kwargs)
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

    def __init__(self, *args, **kwargs):
        self.response_data = {'error': [], 'data': []}
        self.data = {}
        self.code = status.HTTP_200_OK

    def get_serializer_class(self):
        if self.action in ['create_account']:
            return CreateUserAccountSerializer
        if self.action in ['verify_account']:
            return VerifyUserAccountSerializer
        if self.action in ['generate_password']:
            return GeneratePasswordSerializer
        if self.action in ['choose_winner']:
            return None
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

                subject = 'Welcome '
                message_description = 'Email Registration'
                to_email = kwargs['data']['email']
                user = kwargs['data']['first_name'] + \
                    kwargs['data']['last_name']
                template_file = 'email-create-user'
                user_id = (
                    User.objects.filter(
                        email=kwargs['data']['email']))[0].id

                # Send email with celery task
                send_email.delay(
                    subject,
                    to_email,
                    user,
                    user_id,
                    template_file,
                    message_description)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            if serializer:
                serializer.instance.delete()
            logging.getLogger('error_logger').exception(
                "[API - create_account] - Error: " + str(e))
            self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_data['error'].append(
                "[API - UserView] - Error: " + str(e))
        return Response(self.response_data, status=self.code)

    @validate_type_of_request
    @action(methods=['post'], detail=False)
    def verify_account(self, request, *args, **kwargs):
        '''This method allows to verify a new account'''
        try:
            serializer = VerifyUserAccountSerializer(data=kwargs['data'])

            if serializer.is_valid():

                try:
                    user = get_object_or_404(
                        User.objects.filter(
                            id=kwargs['data']['user_id']))
                    user.is_active = True
                    user.save()

                except Exception as e:
                    self.code = status.HTTP_404_NOT_FOUND
                    self.response_data['error'].append(
                        "[API - UserView] - Error: " + str(e))
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_data['error'].append(
                "[API - UserView] - Error: " + str(e))
        return Response(self.response_data, status=self.code)

    @validate_type_of_request
    @action(methods=['post'], detail=False)
    def generate_password(self, request, *args, **kwargs):
        '''This method allows to asign password'''
        try:
            user = User.objects.get(id=kwargs['pk'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = GeneratePasswordSerializer(user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                user.set_password(serializer.data.get('password'))
                user.save()
                self.code = status.HTTP_204_NO_CONTENT
            else:
                self.code = status.HTTP_400_BAD_REQUEST
                self.response_data['error'] = serializer.errors

        except Exception as e:
            self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_data['error'].append(
                "[API - UserView] - Error: " + str(e))
        return Response(self.response_data, status=self.code)

    @validate_type_of_request
    @action(methods=['get'], detail=False)
    def choose_winner(self, request, *args, **kwargs):
        '''This method allows to verify a new account'''
        try:
            '''Exclude users who haven't activated their account and also,
            those who that haven't assigned a password'''
            user_list = User.objects.exclude(Q(password='') & (
                Q(is_active=False)) & (Q(is_deleted=False)))

            if (len(user_list) > 0):
                random_winner = random.randint(1, len(user_list) + 1)
                user_winner = User.objects.get(pk=random_winner)
                self.data['full_name'] = "{} {}".format(
                    user_winner.first_name, user_winner.last_name)
                self.data['email'] = user_winner.email
                self.response_data['data'].append(self.data)
            else:
                self.response_data['data'].append(
                    {"There isn't enough activate users"})
                self.code = status.HTTP_204_NO_CONTENT

        except Exception as e:
            self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_data['error'].append(
                "[API - UserView] - Error: " + str(e))
        return Response(self.response_data, status=self.code)
