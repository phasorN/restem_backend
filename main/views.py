from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from main.serializers import UserSerializer, ExpenseSerializer
from main import models

from rest_condition import And, Or
from rest_framework import generics, status
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from oauth2_provider.models import AccessToken

from django.contrib.auth.hashers import make_password

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'expenses': reverse('expenses-list', request=request, format=format)
    })

class IsReadyOnlyRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class IsPostRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsUserItself(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class UserSelfDetailsOrCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [Or(
	                        # Only GET and POST allowed, all other are Not Allowed.
	                        And(IsReadyOnlyRequest, permissions.IsAuthenticated), # Any authenticated user can get its details.
	                        (IsPostRequest),    # Anyone should be allowed to POST, i.e. to create new user.
	                        )]

    def get_queryset(self):
        return models.User.objects.filter(pk = self.request.user.pk)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [And(IsUserItself, permissions.IsAuthenticated)]  # Only UserItself should be allowed to see/update/delete the User.
    queryset = models.User.objects.all()
    serializer_class = UserSerializer


class ExpensesList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return models.Expense.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpensesDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]  # Only Owner should be allowed to see the Expense.
    queryset = models.Expense.objects.all()
    serializer_class = ExpenseSerializer




















