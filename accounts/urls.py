from django.urls import path
from . import views

urlpatterns = [
    path('all_users/', views.UserList.as_view(), name="all_users"),
    path('register/', views.UserRegistration.as_view(), name="register"),
    path('login/', views.UserLogin.as_view(), name="login"),
    path('view_user/', views.ViewUser.as_view(), name="profile"),
    path('change_password/', views.ChangePassword.as_view(), name="set_password"),
    path('reset_password_mail/', views.SendPasswordEmail.as_view(), name="send_password_mail"),
    path('reset_password/<uid>/<token>/', views.ForgotPassword.as_view()),
    path('update_user/', views.UpdateUser.as_view(), name='update_user'),
    path('logout/', views.Logout.as_view()),

    #google
    path('google/login/', views.GoogleLogin.as_view(), name='google_login'),
    path('google/login/callback/', views.GoogleCallback.as_view(), name='google_callback'),

    #facebbok
    path('facebook/login/',  views.FacebookLogin.as_view(), name='facebook_login'),
    path('facebook/login/callback/',  views.FacebookCallback.as_view(), name='facebook_callback'),
]