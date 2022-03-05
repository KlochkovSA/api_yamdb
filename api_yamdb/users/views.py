from api_yamdb.settings import EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import Roles, User
from .paginations import UsersPagination
from .permissions import IsAdmin, IsSuperuser
from .serializers import (CheckConfirmationCode, SignupSerializer,
                          UserViewSerializer)

CONFIRMATION_CODE_LEN = 20


class Signup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = default_token_generator.make_token(
            serializer.save(role=Roles.USER)
        )
        send_mail(
            subject='Confirmation code',
            message=f'{confirmation_code}',
            from_email=EMAIL,
            recipient_list=[serializer.data['email']],
            fail_silently=False
        )
        return Response(data=serializer.data)


class Token(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CheckConfirmationCode(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserViewSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated, IsSuperuser | IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=username', )
    pagination_class = UsersPagination

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.user.role == Roles.USER:
            serializer.validated_data['role'] = Roles.USER
        serializer.save()
        return Response(serializer.data)
