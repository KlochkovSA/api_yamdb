from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, mixins, serializers
from reviews.models import Review, Comment, Category, Genre, Title
from .permissions import OwnerOrReadOnly, ReadOnly, ModeratorPermission #AdminPermission
from .serializers import (ReviewSerializers, CommentSerializers,
                          CategorySerializer, GenreSerializer, TitleSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        if self.request.user.role == 'mr':
            return (ModeratorPermission())
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        if self.request.user.role == 'mr':
            return (ModeratorPermission())
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class CategoryViewSet(viewsets.ModelViewSet):

class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    # permission_classes = (AdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializer
