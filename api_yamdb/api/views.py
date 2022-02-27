from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, mixins, serializers, permissions
from reviews.models import Review, Comment, Category, Genre, Title
from .permissions import OwnerOrReadOnly, ReadOnly, ModeratorPermission, IsAdmin, ReviewPermissions, RetrieveUpdateDestroyPermission
from .serializers import (ReviewSerializers, CommentSerializers,
                          CategorySerializer, GenreSerializer, TitleSerializerGET)

from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework import permissions


class ReviewListCreateSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (OwnerOrReadOnly,)
    serializer_class = ReviewSerializers

    def perform_create(self, serializer):
        author = self.request.user
        text = self.request.data.get('text')
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        reviews = Review.objects.filter(author=author, title=title)
        if reviews.count() > 0:
            return True

        serializer.save(title=title, author=author, text=text)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.review.all()
        return queryset

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if self.action == 'retrieve':
                return (ReadOnly(),)
            if self.request.user.role == 'mr':
                return (ModeratorPermission())
        return super().get_permissions()


class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializers
    permission_classes = (RetrieveUpdateDestroyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.review.all()
        return queryset

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs["review_id"]
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def get_permissions(self):
        if self.request.user.is_authenticated:
            if self.action == 'retrieve':
                return (ReadOnly(),)
            if self.request.user.role == 'mr':
                return (ModeratorPermission())
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializerGET
    permission_classes = (permissions.AllowAny,)
