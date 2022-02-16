from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from server.authentication.models import User
from server.authentication.serializers import RegSerializer, LoginSerializer, UsersSer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegSerializer

    def post(self, request):
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=request.data.get('email'))

        return Response({'Token': user.token}, status=status.HTTP_200_OK)


class UserListView(APIView):
    serializer_class = UsersSer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = UsersSer(users, many=True, context={'request': request})
        return Response(serializer.data)
