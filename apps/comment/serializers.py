from rest_framework import serializers

from apps.comment.models import Comment
from apps.post.models import Post


class CommentSerializer(serializers.ModelSerializer):
    author_info = serializers.SerializerMethodField()
    replies_count = serializers.ReadOnlyField()
    is_reply = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "author",
            "author_info",
            "replies_count",
            "post",
            "parent",
            "is_reply",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "is_active"]

    def get_author_info(self, obj):
        author = obj.author

        return {
            "id": author.id,
            "username": author.username,
            "full_name": author.full_name,
            "avatar": author.avatar.url if author.avatar else None,
        }


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "post", "parent"]
        read_only_fields = ["author"]

    def validate_parent(self, value):
        is_post_published = Post.objects.filter(
            id=value.id, status="published"
        ).exists()

        if not is_post_published:
            raise serializers.ValidationError("Post is not published")

        return value

    def validate_parent(self, value):
        if value:
            post_data = self.initial_data.get("post")
            if post_data:
                if value.post.id != int(post_data):
                    raise serializers.ValidationError(
                        "Parent comment must belong to the same post."
                    )
        return value

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user

        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]


class CommentDetailSerializer(CommentSerializer):
    replies = serializers.SerializerMethodField()

    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ["replies"]

    def get_replies(self, obj):
        replies = obj.replies.filter(is_active=True).order_by("created_at")

        return CommentSerializer(replies, many=True, context=self.context).data
