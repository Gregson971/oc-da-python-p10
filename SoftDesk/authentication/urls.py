from rest_framework_nested import routers

from .views import UserViewSet


user_router = routers.SimpleRouter()
user_router.register("users", UserViewSet, basename="users")
