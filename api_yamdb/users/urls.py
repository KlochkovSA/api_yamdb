from django.urls import path

from .views import Signup

app_name = 'users'

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup')
]
