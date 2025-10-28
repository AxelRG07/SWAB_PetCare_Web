from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'tipo']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            validated_data['password'] = make_password(validated_data['password'])
            return super().create(validated_data)