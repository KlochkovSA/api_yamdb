from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Review, Comment
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import ReviewSerializers, CommentSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet:
    pass


class GenreViewSet:
    pass


class TitleViewSet:
    pass
