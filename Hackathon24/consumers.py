from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class PrinterConsumer(AsyncWebsocketConsumer):
    groups = ["general"]

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("sprinter-id-0001", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    async def send_to(self, event):
        code = event["code"]
        await self.send(text_data=code)

    async def disconnect(self, close_code):
        print("Loss connection")
