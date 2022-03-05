from rest_framework import serializers


def validate_review(review):
    if review.exists():
        error_message = 'Нельзя написать больше одного отзыва'
        raise serializers.ValidationError(error_message)
