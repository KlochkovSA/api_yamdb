from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import Signup, UsersViewSet

router = SimpleRouter()

app_name = 'users'

router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', Signup.as_view(), name='signup'),
    path('auth/token/', TokenObtainPairView.as_view(), name='signup'),
    path('', include(router.urls)),
]
# urlpatterns += router.urls