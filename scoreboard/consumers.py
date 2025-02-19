import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Called when a client connects to the WebSocket"""
        self.score_id = self.scope["url_route"]["kwargs"]["score_id"]
        self.group_name = f"score_{self.score_id}" 

        # Join WebSocket group for this score
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Called when a client disconnects"""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def update_scoreboard(self, event):
        """Called when a score changes, broadcasting to all clients"""
        await self.send(text_data=json.dumps(event["data"]))