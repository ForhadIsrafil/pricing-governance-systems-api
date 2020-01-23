from django.conf import settings
from rest_framework import serializers
from rest_framework import status
import json
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
import uuid
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.compat import authenticate
from django.db import transaction
from .models import UserInfo
from django.contrib.auth.models import User


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False, write_only=True
    )
    token = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj['user'])
        return token.key

    def get_id(self, obj):
        return obj['user'].id

    def get_name(self, obj):
        return obj['user'].username

    def get_email(self, obj):
        return obj['user'].email

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomValidation(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, detail, field, status_code):
        self.detail = {
            "user": {
                field: [
                    force_text(detail)
                ]
            }
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username','email', 'password')

        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data["username"], email=validated_data["email"])
        user.set_password(raw_password=validated_data["password"])

        user.is_staff = True
        user.is_superuser = False
        user.is_active = True
        user.save()

        return user

    def validate(self, validated_data):
        arr = []
        for email in User.objects.all().values_list('email',flat=True):
            arr.append(email)

        if validated_data.get('email') in arr :
            raise serializers.ValidationError({'email': ['A user with that email already exists.']},
                                              status.HTTP_400_BAD_REQUEST)
        data = super(UserSerializer, self).validate(validated_data)
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True, write_only=True)

    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = ('id', 'user','username', 'email', 'type')


    def get_id(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    @transaction.atomic
    def create(self, validated_data):

        user = UserSerializer.create(UserSerializer(), validated_data=validated_data.pop('user'))
        user_save = transaction.savepoint()
        userinfo, created = UserInfo.objects.update_or_create(user=user,
                                                              type = validated_data.get('type')
                                                              )

        try:
            # open transaction still contains user.save() and userinfo.save()
            transaction.savepoint_commit(user_save)
        except:
            transaction.savepoint_rollback(user_save)

        # generating auth token
        token = Token.objects.create(user=user)
        return userinfo

    def validate(self, data):
        initial_data = self.initial_data
        # start: Checking  confirm password
        password_matching_response = self.is_password_matched(initial_data['password'],
                                                              initial_data['confirm_password'])
        if password_matching_response is not True:
            raise serializers.ValidationError('Password and confirm password does not match.',
                                              status.HTTP_400_BAD_REQUEST)
        # end: Checking  confirm password
        data = super(UserInfoSerializer, self).validate(data)
        return data

    def is_password_matched(self, user_password, user_confirm_password):
        if user_password != user_confirm_password:
            return False
        return True
