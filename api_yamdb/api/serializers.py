from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime as dt
from statistics import mean

from reviews.models import (Category, Comment, Genre,
                            Title, Titles_genres, Review)


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

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            Titles_genres.objects.create(
                genre=genre, title=title)
        return title

    def validate_year(self, value):
        current_year = dt.datetime.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год рождения!')
        return value


class TitleSerializerGET(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        rating = []
        for review in reviews:
            rating.append(review.score)
            return round(mean(rating))


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
