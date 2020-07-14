from django.urls import re_path, include
from vkauth.views import LoginView, FriendsView


urlpatterns = [
    re_path('index', LoginView.as_view(), name='login'),
    re_path('friends', FriendsView.as_view(), name='friends'),
    re_path('', include('social_django.urls', namespace='social')),
]
