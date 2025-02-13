from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatRoom


def home(request):
    rooms = ChatRoom.objects.prefetch_related('messages')
    return render(request, 'home.html', {
        'rooms': rooms,
    })


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def room(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    user_ip = get_client_ip(request)
    rooms = ChatRoom.objects.prefetch_related('messages')
    return render(request, 'chat/room.html', {
        'room_name': room.name,
        'user_ip': user_ip,
        'rooms': rooms,
    })


def new_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        if room_name:
            # Redirect to the newly created room
            return redirect('room', room_name=room_name)
    return render(request, 'new_room.html')

def delete_room(request, id):
    get_object_or_404(ChatRoom, id=id).delete()
    return redirect('home')
