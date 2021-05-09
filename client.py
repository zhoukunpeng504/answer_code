# coding:utf-8
# write by zhou
# client 客户端的实现
from twisted.internet import  reactor,protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import TCP4ClientEndpoint
import json


class Client(LineReceiver):
    '''
    client 协议的具体实现
    '''
    def __init__(self,):
        LineReceiver.__init__(self)
        self.client_id = None

    def connectionMade(self):
        self.client_id = self.factory.client_id
        print("connection made ,client_id: ", self.client_id)
        self.sendLine(self.client_id.encode())

    def lineReceived(self, line):
        try:
            line = line.decode('utf-8')
        except:
            pass
        else:
            try:
                _  = json.loads(line)
                msg_from = _['send_from']
                content = _['content']
                print('received data: %s' % line)
            except Exception as e :
                print('data format is not right! please check it . data: ', line)

    def connectionLost(self, reason):
        print(b'connection lost, client_id: ' ,  self.client_id)

@inlineCallbacks
def connect_to_server(client_id):
    end_point = TCP4ClientEndpoint(reactor,"127.0.0.1", 8003) # 连接到服务器
    client_factory = protocol.ReconnectingClientFactory()  # 自动重连
    client_factory.protocol = Client
    client_factory.client_id = client_id
    client_protocol = yield end_point.connect(client_factory)  # 设置所使用的的协议

# 客户端ID为： 22222222222222222222222222222222
connect_to_server('22222222222222222222222222222222')
reactor.run()