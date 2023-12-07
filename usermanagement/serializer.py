from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'first_name','last_name','username','password','email','is_superuser','last_login']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # token = super().get_token(user)
        token = RefreshToken.for_user(user)
        # Add custom claims
        token['name'] = user.username
        # Add more custom fields from your custom user model, If you have a
        # custom user model.
        # ...

        return token