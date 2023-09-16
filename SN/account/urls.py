from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/',views.User_RegistrationView.as_view(),name='register'),
    path('login/',views.User_LoginView.as_view(),name='login'),
    path('logout/',views.User_LogoutView.as_view(),name='logout'),
    path('profile/<int:user_id>/',views.User_ProfileView.as_view(),name='profile'),
    path('reset/',views.Password_ResetView.as_view(),name='password_reset'),
    path('reset/done/',views.Password_Reset_DoneView.as_view(),name='password_reset_done'),
    path('confirm/<uidb64>/<token>/',views.Password_Reset_ConfirmView.as_view(),name='password_reset_confirm'),
    path('confirm/complete',views.Password_Reset_CompleteView.as_view(),name='password_reset_complete'),
    path('follow/<int:user_id>/',views.User_FollowView.as_view(),name='follow'),
    path('unfollow/<int:user_id>/',views.User_UnfollowView.as_view(),name='unfollow'),
    path('edit/',views.User_Profile_ChangeView.as_view(),name='edit'),
]