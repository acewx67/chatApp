from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from . models import Chat,Group
import json
from channels.db import database_sync_to_async
class MySyncConsumer(SyncConsumer):
    group = None
    def websocket_connect(self,event):
        print('websocket connection established...',event)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        try:
            MySyncConsumer.group = Group.objects.filter(name=self.group_name).first()
        except:
            MySyncConsumer.group = None
        print(self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)
        self.send({
            'type':'websocket.accept',
        })
        
        

    def websocket_receive(self,event):
        print('msg received from client',event)
        async_to_sync(self.channel_layer.group_send)(self.group_name,{
            'type':'chat.msg',
            'msg':event['text']
        })
        content = json.loads(event['text'])
        print('content',content['msg'])
        group = Group.objects.get(name=self.group_name)
        # Chat.objects.create(message=content['msg'],group=MySyncConsumer.group)
        Chat.objects.create(message=content['msg'],group=group)
        # print(MySyncConsumer.group)

    def chat_msg(self,event):
        print('msg...',event)
        print('actual Data',event['msg'])
        self.send({
            'type':'websocket.send',
            'text':event['msg']
        })
    
    def websocket_disconnect(self,event):
        print('websocket disconnected...',event)
        print('channel layer',self.channel_layer) #get default channel layer
        print('channel name',self.channel_name)
        # print(self.group_name)
        # print('pppppppppppppp')
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    group = None
    async def websocket_connect(self,event):
        print('websocket connection established...',event)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        # try:
        #     MySyncConsumer.group = Group.objects.filter(name=self.group_name).first()
        # except:
        #     MySyncConsumer.group = None
        print(self.group_name)
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.send({
            'type':'websocket.accept',
        })
        
        

    async def websocket_receive(self,event):
        print('msg received from client',event)
        await self.channel_layer.group_send(self.group_name,{
            'type':'chat.msg',
            'msg':event['text']
        })
        content = json.loads(event['text'])
        print('content',content['msg'])
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        # Chat.objects.create(message=content['msg'],group=MySyncConsumer.group)
        await database_sync_to_async(Chat.objects.create)(message=content['msg'],group=group)
        # print(MySyncConsumer.group)

    async def chat_msg(self,event):
        print('msg...',event)
        print('actual Data',event['msg'])
        await self.send({
            'type':'websocket.send',
            'text':event['msg']
        })
    
    async def websocket_disconnect(self,event):
        print('websocket disconnected...',event)
        print('channel layer',self.channel_layer) #get default channel layer
        print('channel name',self.channel_name)
        # print(self.group_name)
        # print('pppppppppppppp')
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        raise StopConsumer()