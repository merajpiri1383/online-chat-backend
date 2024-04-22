import json.scanner
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer 
import json

class MessageChatConsumer(AsyncWebsocketConsumer ) : 
    
    async def connect(self): 
        print("connect")
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = f"group_{self.chat_id}"
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept() 
    
    async def receive(self,text_data=None,byte_data=None) : 
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type" : "message.send"
            }
        )
        
    async def disconnect(self,close_code) : 
        print("disconnect")
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
    
    async def message_send(self,envent) : 
        await self.send(json.dumps({
            "type" : "message.send"
        }))
        