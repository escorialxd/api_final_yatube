from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from posts.models import Post, Group
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsAuthorOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        return [AllowAny()]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def get_post(self):
        """Получаем объект поста по параметру post_id из URL."""
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(id=post_id)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsAuthorOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = [SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return self.request.user.follower.all()

    def get_permissions(self):
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
