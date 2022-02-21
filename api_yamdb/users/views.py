import random
import string

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (MyTokenObtainPairSerializer, SignupSerializer,
                          UserViewSerializer)
from .permissions import AdminPermission

CONFIRMATION_CODE_LEN = 20


def get_confirmation_code():
    return ''.join(random.choices(
        string.digits + string.ascii_uppercase,
        k=CONFIRMATION_CODE_LEN
    ))


class Signup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                subject='Confirmation code',
                message=f'{get_confirmation_code()}',
                from_email='any_mail@yandex.ru',
                recipient_list=[serializer.data['email']],
                fail_silently=False
            )
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserViewSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, AdminPermission)


class Profile(viewsets.GenericViewSet):
    pass