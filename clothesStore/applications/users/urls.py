from django.urls import path

# required views
from .views import (
    UserRegisterView,
    CodeVerificationView,
    LoginUserView,
    LogoutView,
    UpdatePassword,
    ListUsersView,
    BlockUserView,
    AllowUser,
    DetailsUserView
)

app_name='users_app'

urlpatterns = [
    path(
        'register/', 
        UserRegisterView.as_view(),
        name='register'
    ),
    path(
        'verify-account/<pk>/', 
        CodeVerificationView.as_view(),
        name='user-verification'
    ),
    path(
        'login/', 
        LoginUserView.as_view(),
        name='login'
    ),
    path(
        'logout/', 
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'update-password/', 
        UpdatePassword.as_view(),
        name='update-password'
    ),
    path(
        'users/', 
        ListUsersView.as_view(),
        name='users'
    ),
    path(
        'block/<pk>', 
        BlockUserView.as_view(),
        name='block-user'
    ),
    path(
        'allow/<pk>', 
        AllowUser.as_view(),
        name='allow-user'
    ),
    path(
        'user/details/<pk>', 
        DetailsUserView.as_view(),
        name='user-details'
    ),
]

