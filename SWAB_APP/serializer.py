from rest_framework import serializers

from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'username', 'first_name', 'last_name', 'email', 'tipo'