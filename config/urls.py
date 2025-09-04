from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.user.urls")),
    path("api/v1/posts/", include("apps.post.urls")),
    path("api/v1/comments/", include("apps.comment.urls")),
]
