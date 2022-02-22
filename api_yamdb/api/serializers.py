from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from statistics import mean

from reviews.models import Category, Comment, Genre, Title, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializerGET(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        score = Review.objects.filter(title=obj.id).score
        return round(mean(score))


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
