from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')

api_v1_patterns = [
    path('jwt/create/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(),
         name='token_verify'),

    path('', include(router.urls)),

    path('posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='post-comments'),
    path('posts/<int:post_id>/comments/<int:comment_id>/',
         CommentViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
             'patch': 'partial_update',
             'delete': 'destroy'
         }),
         name='post-comment-detail'),
]

urlpatterns = [
    path('v1/', include(api_v1_patterns))
]
