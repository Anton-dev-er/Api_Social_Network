from django.urls import path
from .views import UnLikePostView, LikePostView, PostView


app_name = 'social_network'
urlpatterns = [
    path('post/', PostView.as_view()),
    path('like/', LikePostView.as_view()),
    path('unlike/', UnLikePostView.as_view()),
]