from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer 
import json

class MessageChatConsumer(AsyncWebsocketConsumer ) : 
    
    async def connect(self): 
        print("connect")
        self.data = []
        await self.accept() 
    
    async def receive(self,text_data=None,byte_data=None) : 
        self.data = json.loads(text_data)
        # getting chats id and group id and create a group for each one ... 
        if self.data["type"] == "start" : 

            for chat in self.data["chats"] : 
                print(chat["id"])
                await self.channel_layer.group_add("chat_" + str(chat["id"]),self.channel_name)
            
            for group in self.data["groups"] : 
                print(group["id"])
                await self.channel_layer.group_add("group_" + str(group["id"]),self.channel_name)
            
            
        if self.data["type"] == "message.send" :  
            print("get data")
            print(self.data)
            print(self.channel_layer)
            print(self.channel_name)
            print(self.data["id"])
            await self.channel_layer.group_send(
                self.data["id"],
                {
                    "type" : "message_send",
                    "id" : self.data["id"]
                }
            )
        
    async def disconnect(self,close_code) : 
        print("disconnect")
        if self.data : 
            for chat in self.data["chats"] : 
                await self.channel_layer.group_discard("chat_" + str(chat["id"]),self.channel_name)
            
            for group in self.data["groups"] : 
                await self.channel_layer.group_discard("group_" + str(group["id"]),self.channel_name) 
    
    async def message_send(self,data) : 
        print("send_message")
        print(data)
        await self.send(json.dumps({"type":"message.send"}))
