from django.conf.urls import url
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
import json
import weakref 
import time


class camera1(AsyncWebsocketConsumer):

	too_close = False

	async def connect(self):
        await self.channel_layer.group_add("camera1", self.channel_name)
        await self.accept()
        message("yeet")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("security", self.channel_name)

    async def receive(self, text_data):
    	print("reciveing data")
    	data = json.loads(text_data)
        print(data)

    async def message(self, event):
        print("sending data")
        await self.send(text_data=json.dumps(event['message']))


class camera2(AsyncWebsocketConsumer):

	too_close = False

	async def connect(self):
        await self.channel_layer.group_add("camera1", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("security", self.channel_name)

    async def receive(self, text_data):
    	print("reciveing data")
    	data = json.loads(text_data)
        print(data)

    async def message(self, event):
        print("sending data")
        await self.send(text_data=json.dumps(event['message']))


application = ProtocolTypeRouter({
    "websocket": URLRouter([
        url("camera1", camera1),
        url("camera2", camera2),
    ]),
})