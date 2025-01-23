from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class Chating(WebsocketConsumer):
    def connect(self):
        from .models import ChatRoom
        # Get the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        self.ip = self.scope['client'][0]

        # Get or create the chat room
        self.room, created = ChatRoom.objects.get_or_create(name=self.room_name)

        # Add the user's channel to the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        # Accept the connection
        self.accept()

        # Send the chat history to the user
        messages = self.room.messages.order_by('timestamp')  # Fetch chat history
        for message in messages:
            self.send(text_data=json.dumps({
                "message": message.content,
                "sender": message.sender.username if message.sender else "Anonymous",
                "sender_ip": message.sender_ip,
                "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }))

    def disconnect(self, close_code):
        # Remove the user from the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        from .models import Message
        # Parse the incoming WebSocket message
        data = json.loads(text_data)
        msg = data["message"]

        # Save the message to the database
        message = Message.objects.create(
            room=self.room,
            sender=self.user if self.user.is_authenticated else None,
            sender_ip=self.ip,
            content=msg
        )

        # Broadcast the message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type": "chat_messages",
                "messages": msg,
                "sender": str(self.user) if self.user.is_authenticated else "Anonymous",
                "ip": self.ip,
            }
        )

    def chat_messages(self, event):
        # Send the message to WebSocket clients
        self.send(text_data=json.dumps({
            "message": event["messages"],
            "sender": event["sender"],
            "sender_ip": event["ip"],
        }))














# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync


# class Chating(WebsocketConsumer):
#     def connect(self):
#         # Get the room name from the URL
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.user = self.scope['user']  # Get the current user
#         self.ip = self.scope['client'][0]  # Retrieve the client's IP address

#         # Add the user's channel to the group for the chat room
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_name, self.channel_name
#         )
        
#         # Accept the WebSocket connection
#         self.accept()

#     def disconnect(self, code):
#         # Remove the user's channel from the group when they disconnect
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_name, self.channel_name
#         )

#     def receive(self, text_data=None, bytes_data=None):
#         # Parse the incoming WebSocket message
#         data = json.loads(text_data)
#         msg = data["message"]

#         # Broadcast the message to the group with the sender's username and IP
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_name,
#             {
#                 "type": "chat_messages",
#                 "messages": msg,
#                 "sender": str(self.scope['user']),  # Include the sender's username
#                 "ip": self.ip,  # Include the sender's IP address
#             }
#         )

#     def chat_messages(self, event):
#         # Send the message, sender info, and sender IP to the WebSocket
#         msg = event["messages"]
#         sender = event["sender"]
#         sender_ip = event["ip"]
#         self.send(
#             text_data=json.dumps(
#                 {
#                     "message": msg,
#                     "sender": sender,
#                     "sender_ip": sender_ip,  # Include the sender's IP address
#                 }
#             )
#         )











# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync

# class Chating(WebsocketConsumer):
#     def connect(self):
#         # Get the room name from the URL
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.user = self.scope['user']  # Get the current user
        
#         # Add the user's channel to the group for the chat room
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_name, self.channel_name
#         )
        
#         # Accept the WebSocket connection
#         self.accept()

#     def disconnect(self, code):
#         # Remove the user's channel from the group when they disconnect
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_name, self.channel_name
#         )

#     def receive(self, text_data=None, bytes_data=None):
#         # Parse the incoming WebSocket message
#         data = json.loads(text_data)
#         msg = data["message"]

#         # Broadcast the message to the group with the sender's username
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_name,
#             {
#                 "type": "chat_messages",
#                 "messages": msg,
#                 "sender": str(self.scope['user']),  # Include the sender's username
#             }
#         )

#     def chat_messages(self, event):
#         # Send the message and sender info to the WebSocket
#         msg = event["messages"]
#         sender = event["sender"]
#         self.send(
#             text_data=json.dumps(
#                 {
#                     "message": msg,
#                     "sender": sender,  # Include the sender's username
#                 }
#             )
#         )












# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# class Chating(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_name,self.channel_name
#         )
#         self.accept()
    
#     def disconnect(self, code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_name,self.channel_name
#         )
    
#     def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         msg = data["message"]
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_name,{"type":"chat_messages","messages":msg ,"user": str(self.scope['user'])}
#         )
#     def chat_messages(self,event):
#         msg = event["messages"]
#         self.send(text_data=json.dumps({"message": msg,"user":event["user"]}))