from django.urls import path

from Auth.api.views import get_all_users, create_user,get_user



urlpatterns = [
    path('users/',get_all_users,name='get_all_users'),
    path('users/create',create_user,name='create_user'),
    path('users/<int:pk>',get_user,name='get_user'),
]