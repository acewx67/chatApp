from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('websocket connection established...',event)
        self.send({
            'type':'websocket.accept',
        })
        async_to_sync(self.channel_layer.group_add)('Global',self.channel_name)

    def websocket_receive(self,event):
        print('msg received from client',event)
        self.channel_layer.group_send('Global',{
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
        async_to_sync(self.channel_layer.group_discard)('global',self.channel_name)
        raise StopConsumer()
