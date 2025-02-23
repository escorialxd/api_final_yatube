from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Post, Group, Follow
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .mixins import DynamicPermissionMixin


class PostViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()


class GroupViewSet(DynamicPermissionMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def get_post(self):
        """Получаем объект поста по параметру post_id из URL."""
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(id=post_id)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(
    DynamicPermissionMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    enforce_auth_for_safe_methods = True
    serializer_class = FollowSerializer
    filter_backends = [SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
