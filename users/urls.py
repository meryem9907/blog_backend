from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import RegisterView, LogoutView, MeView, DeleteUserView, UpdateUserView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"), # login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), 
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("delete/user/", DeleteUserView.as_view(), name="delete_user"),
    path("update/user/", UpdateUserView.as_view(), name="update_user")
]