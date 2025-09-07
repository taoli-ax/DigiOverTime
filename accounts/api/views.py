from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.api.serializers import AccountSerializer


# Create your views here.
class AccountViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)


