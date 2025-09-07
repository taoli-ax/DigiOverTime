from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers, exceptions


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']

class LoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignUpSerializer(ModelSerializer):
    username = serializers.CharField(min_length=6, max_length=20)
    password = serializers.CharField(min_length=8, max_length=15)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields=['username', 'password', 'email']

    def validate(self, data):
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({"message":"Username has been occupied."})
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({"message":"Email has been occupied."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'].lower(),
            password=validated_data['password'],
            email=validated_data['email'].lower(),
        )
        return user

