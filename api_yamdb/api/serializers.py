import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (Category, Comment, Genre, Title,
                            Review)
from .validators import validate_review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializerPOST(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')

    def validate_year(self, value):
        current_year = dt.datetime.today().year
        if current_year < value < 0:
            raise serializers.ValidationError('Проверьте год создания!')
        return value


class TitleSerializerGET(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class ReviewSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')

    # Проверка уникального отзыва
    def create(self, validated_data):
        title_id = self.context['view'].kwargs['title_id']
        author_data = self.context['request'].user
        title = get_object_or_404(Title, id=title_id)
        review = Review.objects.filter(title=title, author=author_data)
        validate_review(review)
        return Review.objects.create(title=title,
                                     author=author_data,
                                     **validated_data)


class CommentSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('review',)
