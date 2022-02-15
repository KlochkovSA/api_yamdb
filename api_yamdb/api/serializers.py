from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment


class ReviewSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'pub_date',)

    # Проверка уникального отзыва
    def create(self, validated_data):
        title_data = validated_data.get('title')
        author_data = serializers.CurrentUserDefault()
        review = Review.objects.filter(title=title_data, author=author_data)
        if review.exists():
            raise OverflowError('Нельзя написать больше одного отзыва')
        else:
            new_review = Review.objects.create(**validated_data)
            return new_review


class CommentSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        models = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date',)
