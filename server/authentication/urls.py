from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, UserListView

app_name = 'authentication'
urlpatterns = [
    path('reg/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('users/', UserListView.as_view()),
]
