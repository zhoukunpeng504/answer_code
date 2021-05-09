# coding:utf-8
# write by zhou
# 消息推送通道 server端的实现
from twisted.application.service import  Application,Service
from twisted.internet import  reactor,protocol
from twisted.protocols.basic import LineReceiver
import json


all_online_client = {}


class Server(LineReceiver):

    def __init__(self):
        LineReceiver.__init__(self)
        self.client_id = None

    def connectionMade(self):
        print("connection made")

    def lineReceived(self, line):
        global  all_online_client
        print(b'received data: %s' % line)
        try:
            line = line.decode('utf-8')
        except:
            pass
        else:
            if self.client_id == None:
                if len(line) == 32:
                    self.client_id = line
                    all_online_client[self.client_id] = self
                else:
                    self.transport.loseConnection()

            else:
                try:
                    recv_data = json.loads(line)
                    send_to = recv_data['send_to']
                    content = recv_data['content']
                except Exception as e:
                    print('data format is not right! please check it, data: ', line)
                else:
                    if send_to in all_online_client:
                        try:
                            all_online_client[send_to].sendLine(json.dumps({"send_from":self.client_id,
                                                                            'content': content}).encode('utf-8'))
                        except Exception as e:
                            print("send_data_error :", str(e))


    def connectionLost(self, reason):
        print(b'connection lost, clientid: ' ,  self.client_id)
        try :
            all_online_client.pop(self.client_id)
        except:
            pass



factory = protocol.ServerFactory()
factory.protocol = Server
reactor.listenTCP(8003,factory)
reactor.run()