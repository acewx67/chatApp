from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('websocket connection established...',event)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
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
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        raise StopConsumer()
