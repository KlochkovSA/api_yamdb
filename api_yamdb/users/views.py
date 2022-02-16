import random
import string

from django.core.mail import send_mail
from rest_framework.views import APIView

CONFIRMATION_CODE_LEN = 20


def get_confirmation_code():
    return ''.join(random.choices(
        string.digits + string.ascii_uppercase,
        k=CONFIRMATION_CODE_LEN
    ))


class Signup(APIView):
    def post(self, request):
        print(request.data)
        send_mail(
            subject='Confirmation code',
            message=f'{get_confirmation_code()}',
            from_email='any_mail@yandex.ru',
            recipient_list=[request.data.get('email')],
            fail_silently=False
        )
