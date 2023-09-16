from  django.urls import path
from . import views

app_name = 'Home'
urlpatterns = [
    path('',views.Home_PageView.as_view(),name='home'),
    path('post/detail/<int:post_id>/<slug:post_slug>/',views.Post_DetailView.as_view(),name='detail'),
    path('post/delete/<int:post_id>/',views.Delete_PostView.as_view(),name='delete'),
    path('post/update/<int:post_id>/',views.Update_PostView.as_view(),name='update'),
    path('post/create/',views.Create_PostView.as_view(),name='create'),
    path('reply/<int:post_id>/<int:comment_id>/',views.Reply_CommentView.as_view(),name='reply'),
    path('like/<int:post_id>/',views.Post_LikeView.as_view(),name='like'),
]