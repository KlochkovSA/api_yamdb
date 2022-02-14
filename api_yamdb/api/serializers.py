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
        fields = ('id', 'titles', 'text', 'author', 'pub_date',)


class CommentSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        models = Comment
        fields = ('id', 'reviews', 'text', 'author', 'pub_date',)
