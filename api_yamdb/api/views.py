from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Comment, Category, Genre, Title
from .filters import TitleFilter
from .permissions import IsAdmin, OwnerAndStaffPermission
from .serializers import (CommentSerializers, CategorySerializer,
                          GenreSerializer, ReviewSerializers,
                          TitleSerializerGET, TitleSerializerPOST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerAndStaffPermission,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerAndStaffPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review=review_id)

    def perform_create(self, serializer):
        author = self.request.user
        text = self.request.data.get('text')
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title__id=title_id)

        serializer.save(review=review, author=author, text=text)


class CustomViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return (IsAdmin(),)
        return super().get_permissions()


class CategoryViewSet(CustomViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(CustomViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    lookup_url_kwarg = 'titles_id'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    queryset = Title.objects.annotate(rating=Avg('review__score'))
    serializer_class = TitleSerializerPOST

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializerGET
        return TitleSerializerPOST

    def get_permissions(self):
        if (self.action == 'create'
                or self.action == 'partial_update'
                or self.action == 'destroy'):
            return (IsAdmin(),)
        return super().get_permissions()
