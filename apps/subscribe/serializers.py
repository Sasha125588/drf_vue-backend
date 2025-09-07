from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from apps.subscribe.models import (
    PinnedPost,
    Subscription,
    SubscriptionHistory,
    SubscriptionPlan,
)
from apps.post.models import Post


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "price",
            "duration_days",
            "features",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if not data.get("features"):
            data["features"] = {}

        return data


class SubscriptionSerializer(serializers.ModelSerializer):

    plan_info = SubscriptionPlanSerializer(source="plan", read_only=True)
    user_info = serializers.SerializerMethodField()
    is_active = serializers.BooleanField()
    days_remaining = serializers.IntegerField()

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "user_info",
            "plan",
            "plan_info",
            "status",
            "start_date",
            "end_date",
            "days_remaining",
            "auto_renew",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]

    def get_user_info(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "full_name": obj.user.full_name,
            "email": obj.user.email,
        }


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["plan"]

    def validate_plan(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Plan is not active")
        return value

    def validate(self, attrs):
        user = self.context["request"].user

        if hasattr(user, "subscription") and user.subscription.status != "expired":
            raise serializers.ValidationError("User already has a subscription")

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["status"] = "pending"
        validated_data["start_date"] = timezone.now()
        validated_data["end_date"] = timezone.now() + timedelta(
            days=validated_data["plan"].duration_days
        )

        return super().create(validated_data)


class PinnedPostSerializer(serializers.ModelSerializer):
    post_info = serializers.SerializerMethodField()

    class Meta:
        model = PinnedPost
        fields = ["id", "post", "post_info", "pinned_at"]
        read_only_fields = ["id", "pinned_at"]

    def get_post_info(self, obj):
        return {
            "id": obj.post.id,
            "title": obj.post.title,
            "slug": obj.post.slug,
            "content": obj.post.content,
            "image": obj.post.image.url,
            "views_count": obj.post.views_count,
            "created_at": obj.post.created_at,
        }

    def validate_post(self, value):
        user = self.context["request"].user

        if value.author != user:
            raise serializers.ValidationError("You are not the author of this post")

        if value.status != "published":
            raise serializers.ValidationError("Post is not published")

        return value

    def validate(self, attrs):
        user = self.context["request"].user

        if not hasattr(user, "subscription") or not user.subscription.is_active:
            raise serializers.ValidationError("User does not have a subscription")

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        return super().create(validated_data)


class SubscriptionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionHistory
        fields = ["id", "action", "description", "metadata", "created_at"]
        read_only_fields = ["id", "created_at"]


class UserSubscriptionStatusSerializer(serializers.Serializer):
    has_subscription = serializers.BooleanField()
    is_active = serializers.BooleanField()
    subscription = SubscriptionSerializer(allow_null=True)
    pinned_post = PinnedPostSerializer(allow_null=True)
    can_pin_posts = serializers.BooleanField()

    def to_representation(self, instance):
        user = instance
        has_subscription = hasattr(user, "subscription")
        subscription = user.subscription if has_subscription else None
        is_active = subscription.is_active if has_subscription else False
        pinned_post = getattr(user, "pinned_post", None) if is_active else None

        return {
            "has_subscription": has_subscription,
            "is_active": is_active,
            "subscription": (
                SubscriptionSerializer(subscription).data if subscription else None
            ),
            "pinned_post": (
                PinnedPostSerializer(pinned_post).data if pinned_post else None
            ),
            "can_pin_posts": is_active,
        }


class PinPostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()

    def validate_post_id(self, value):
        try:
            post = Post.objects.get(id=value, status="published")
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post not found or not published.")

        user = self.context["request"].user
        if post.author != user:
            raise serializers.ValidationError("You can only pin your own posts.")

        return value

    def validate(self, attrs):
        user = self.context["request"].user

        if not hasattr(user, "subscription") or not user.subscription.is_active:
            raise serializers.ValidationError(
                "Active subscription required to pin posts"
            )

        return attrs


class UnpinPostSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context["request"].user

        if not hasattr(user, "pinned_post"):
            raise serializers.ValidationError("No pinned post found")

        return attrs
