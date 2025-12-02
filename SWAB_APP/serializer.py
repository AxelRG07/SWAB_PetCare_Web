from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'tipo', 'groups']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'

class RefugioSerializer(serializers.ModelSerializer):
    mascotas = MascotaSerializer(many=True, read_only=True)
    class Meta:
        model = Refugio
        fields = '__all__'


