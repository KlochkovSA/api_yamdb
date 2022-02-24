from rest_framework import serializers

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя \'me\' недоступно')
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name',
                  'last_name', 'bio')


class CheckConfirmationCode(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
