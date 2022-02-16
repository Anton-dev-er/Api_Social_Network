from django.urls import path, include


urlpatterns = [
    path('auth/', include('server.authentication.urls')),
    path('', include('server.social_network.urls')),
]