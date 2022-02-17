from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from server.authentication.models import User
from server.authentication.serializers import RegSerializer, LoginSerializer

from django.utils import timezone

from server.social_network.models import LikedList


class RegistrationAPIView(APIView):
    serializer_class = RegSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        data = {
            'email': email,
            'password': password,
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=email)
        LikedList.objects.create(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        data = {
            'email': email,
            'password': password,
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=email)
        user.last_login = timezone.now()
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


