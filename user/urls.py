from django.urls import path
from user import views


urlpatterns = [
    path('register/', views.UserRegisterApiView.as_view(), name='register-user'),
    path('login/', views.UserLoginApiView.as_view(), name='login-user'),
    path('logout/', views.UserLogoutApiView.as_view(), name='logout-user'),
]