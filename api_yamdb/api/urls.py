from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentListCreateSet, CommentRetrieveUpdateDestroyAPIView, GenreViewSet,
                    ReviewListCreateSet, ReviewRetrieveUpdateDestroyAPIView, TitleViewSet)

app_name = 'api'

router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewListCreateSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentListCreateSet,
    basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('users.urls')),
    path(
        r'v1/titles/<title_id>/reviews/<review_id>/',
        ReviewRetrieveUpdateDestroyAPIView.as_view(),
        name='api'),
    path(
        'v1/titles/<int:title_id>/reviews/<int:review_id>/'
        'comments/<int:comment_id>/',
        CommentRetrieveUpdateDestroyAPIView.as_view(),
        name='api'
    ),
]
