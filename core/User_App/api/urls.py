from django.urls import path
from User_App.api.views import get_app_users,create_app_users




urlpatterns=[
    path('users/list',get_app_users,name='get_app_users'),
    path('users/create',create_app_users,name='create_app_users'),
]


