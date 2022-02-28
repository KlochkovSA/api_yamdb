from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, mixins
from rest_framework.validators import ValidationError

from reviews.models import Review, Comment, Category, Genre, Title

from .permissions import IsAdmin, OwnerAndStaffPermission
from .serializers import (ReviewSerializers, CommentSerializers,
                          CategorySerializer, GenreSerializer, TitleSerializerGET,
                          TitleSerializerPOST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title=title_id)

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'destroy':
            return [OwnerAndStaffPermission(),]
        return super().get_permissions()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        review = Review.objects.filter(author=self.request.user, title=title)
        if review.count() != 0:
            raise ValidationError('Нельзя написать больше одного отзыва')
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'destroy':
            return [OwnerAndStaffPermission(),]
        return super().get_permissions()

    def perform_create(self, serializer):
        author = self.request.user
        text = self.request.data.get('text')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)

        serializer.save(review=review, author=author, text=text)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return (IsAdmin(),)
        return super().get_permissions()


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return (IsAdmin(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    lookup_url_kwarg = 'titles_id'

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializerGET
        return TitleSerializerPOST

    def get_queryset(self):
        queryset = Title.objects.all()
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        name = self.request.query_params.get('name')
        year = self.request.query_params.get('year')
        if category:
            queryset = queryset.filter(category__slug=category)
        elif genre:
            queryset = queryset.filter(genre__slug=genre)
        elif name:
            queryset = queryset.filter(name__contains=name)
        elif year:
            queryset = queryset.filter(year=year)
        return queryset

    def get_permissions(self):
        if (self.action == 'create'
                or self.action == 'partial_update'
                or self.action == 'destroy'):
            return (IsAdmin(),)
        return super().get_permissions()

