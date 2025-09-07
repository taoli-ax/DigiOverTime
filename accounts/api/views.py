import django.contrib.auth
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.api.serializers import LoginSerializer, UserSerializer, SignUpSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class AccountViewSet(ModelViewSet):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all().order_by('-date_joined')

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = django.contrib.auth.authenticate(username=username, password=password)
        if not user or user.is_anonymous:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
        django.contrib.auth.login(request, user)

        return Response({
            'success':True,
            'user':UserSerializer(instance=user).data},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def signup(self,request):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user= serializer.save()
        return Response(
            UserSerializer(instance=user).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['post'], detail=False)
    def logout(self, request):
        django.contrib.auth.logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

