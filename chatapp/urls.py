from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('new-room', new_room, name='new_room'),
    path('chat/<str:room_name>/', room, name='room'),

]