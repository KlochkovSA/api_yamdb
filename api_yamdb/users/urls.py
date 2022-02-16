from django.urls import include, path

from .views import Signup

urlpatterns = [
    path('auth/signup/', Signup.as_view(), name='signup')
]
