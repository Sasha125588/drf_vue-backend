from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import filters

from apps.post.models import Post
from apps.post.permissions import IsAuthorOrReadOnly
from .models import Comment
from .serializers import (
    CommentCreateSerializer,
    CommentDetailSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)


# Create your views here.
class ComentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["post", "author", "parent"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Comment.objects.filter(is_active=True).select_related(
            "author", "post", "parent"
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer

        return CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(is_active=True).select_related("author", "post")
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return CommentUpdateSerializer

        return CommentDetailSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CommentRepliesView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["post", "is_active", "parent"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).select_related(
            "post", "parent"
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")

    comments = (
        Comment.objects.filter(post=post, is_active=True, parent=None)
        .select_related("author")
        .prefetch_related("replies")
        .order_by("-created_at")
    )

    serializer = CommentSerializer(comments, many=True, context={"request": request})

    return Response(
        {
            "post": {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
            },
            "comments": serializer.data,
            "comments_count": post.comments.filter(is_active=True).count(),
        }
    )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def comment_replies(request, comment_id):
    parrent_comment = get_object_or_404(Comment, id=comment_id, is_active=True)

    replies = (
        Comment.objects.filter(parent=parrent_comment, is_active=True)
        .select_related("author")
        .order_by("-created_at")
    )

    serializer = CommentSerializer(replies, many=True, context={"request": request})

    return Response(
        {
            "parrent_comment": CommentSerializer(
                parrent_comment, context={"request": request}
            ).data,
            "replies": serializer.data,
            "replies_count": replies.count(),
        }
    )
