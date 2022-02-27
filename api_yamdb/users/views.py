import random
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin, IsAdminOrOnlyRead, IsSuperuser
from .serializers import (CheckConfirmationCode, SignupSerializer,
                          UserViewSerializer)

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
        confirmation_code = get_confirmation_code()
        if serializer.is_valid():
            serializer.save(confirmation_code=confirmation_code, role='user')
            send_mail(
                subject='Confirmation code',
                message=f'{confirmation_code}',
                from_email='any_mail@yandex.ru',
                recipient_list=[serializer.data['email']],
                fail_silently=False
            )
            return Response(data=serializer.data)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class Token(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CheckConfirmationCode(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            confirmation_code = serializer.data.get('confirmation_code')
            user = get_object_or_404(User, username=username)
            if confirmation_code == user.confirmation_code:
                token = AccessToken.for_user(user)
                return Response(
                    {'token': f'{token}'},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserViewSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated, IsSuperuser | IsAdmin,)
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if request.user.role == 'user':
                serializer.validated_data['role'] = 'user'
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)


class Profile(viewsets.GenericViewSet):
    pass
