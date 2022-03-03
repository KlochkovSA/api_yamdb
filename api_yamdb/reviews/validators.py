import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = dt.datetime.today().year
    if current_year < value < 0:
        raise ValidationError('Проверьте год создания!')
