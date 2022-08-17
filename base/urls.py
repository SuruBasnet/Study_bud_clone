from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name = "home"),
    path('room/<str:pk>/', views.room , name = "room"),
    path('createroom/' , views.createroom , name= 'createRoom'),
    path('editroom/<str:pk>/' , views.editroom , name= 'editRoom'),
    path('delete-room/<str:pk>/' , views.deleteroom , name= 'deleteRoom'),
    path('delete-message/<str:pk>/' , views.deleteMessage , name= 'deleteMessage'),
    path('login/' , views.loginpage , name= 'login'),
    path('logout/' , views.logoutpage , name= 'logout'),
    path('register/' , views.registerpage , name= 'register'),
    path('profile_page/<str:pk>/' , views.profile_page , name='profilepage'),
    path('edit-user/' , views.editUser , name='edit-user'),
    path('topics/' , views.topicspage , name='topics'),
    path('activity/' , views.activitypage , name='activity'),

    # path('register/' , views.signup , name='signup'),
]