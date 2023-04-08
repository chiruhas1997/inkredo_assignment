from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.Register.as_view(),name='register'),
    path('testing',views.testing,name='register'),
    path('login',views.login,name='login'),
    path('create_home',views.register_home,name='register_home'),
    path('home/<home_name>',views.home,name='home'),
    path('add_room/<home_name>',views.add_room,name='home'),
    path('room/<home_name>/<room_id>',views.room,name='home'),
    path('list_owners/',views.list_owners,name='owners'),
    path('list_homes/<owner>',views.list_homes,name='list_homes'),
    path('list_rooms/<owner>/<homes>', views.list_rooms, name='list_rooms'),
    path('add_images/<home_name>',views.add_images,name = 'add_images'),
    path('list_images/<owner>/<home>', views.list_images, name='list_images'),
]
