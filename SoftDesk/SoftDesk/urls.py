from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.urls import user_router
from project.urls import project_router, issue_router, comment_router, contributor_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(user_router.urls)),
    path("api/", include(project_router.urls)),
    path("api/", include(issue_router.urls)),
    path("api/", include(comment_router.urls)),
    path("api/", include(contributor_router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
