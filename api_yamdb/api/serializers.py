from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


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
