# coding:utf-8
# write by zhou
# 本程序中为了简化逻辑，保持通用性 直接使用了原生的socket。
# 可快速的嵌入到其他业务中
import socket
import json
import time


def push_message(my_client_id : bytes, to_client_id: bytes, content :str):
    '''
    对整个消息推送进行封装
    :param my_client_id: 我的client_id
    :param to_client_id: 我要发送到的客户端的id
    :param content: 我要发送的内容
    :return:
    '''
    assert len(my_client_id) ==  32 and len(to_client_id) == 32,Exception('client_id format error')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1',8003))
    s.sendall(my_client_id+b'\r\n')
    s.sendall(json.dumps({'send_to': to_client_id.decode('utf-8'), 'content': content}).encode('utf-8')+b'\r\n')
    s.close()

if __name__ == '__main__':
    push_message(b'11111111111111111111111111111111', b'22222222222222222222222222222222',
                 json.dumps({'image_content':"", 'check_result': True, "check_time": int(time.time())}))