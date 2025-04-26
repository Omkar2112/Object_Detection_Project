from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

class SendDetectionConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print("Websocket Connected",event)
        async_to_sync(self.channel_layer.group_add)("logs",self.channel_name)
        self.send({
            "type":"websocket.accept"
        })

    def websocket_receive(self,event):
        async_to_sync(self.channel_layer.group_send)("logs",{"type":"logs.message","text":event['text']})
        print("Message Received : ",event['text'])

    def logs_message(self,event):
        print("logs_message activated")
        self.send({"type":"websocket.send","text":event['text']})

    def websocket_disconnect(self,event):
        print("Disconnected")
        async_to_sync(self.channel_layer.group_discard)("logs",self.channel_name)
        raise StopConsumer()
