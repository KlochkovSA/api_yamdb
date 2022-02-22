from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import Signup, Token, UsersViewSet

router = SimpleRouter()

app_name = 'users'

router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', Signup.as_view(), name='signup'),
    path('auth/token/', Token.as_view(), name='signup'),
    path('', include(router.urls)),
]
