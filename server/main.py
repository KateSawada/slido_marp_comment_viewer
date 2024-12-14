import json
import logging

from websocket_server import WebsocketServer


class Websocket_Server:

    def __init__(self, host, port):
        self.server = WebsocketServer(port=port, host=host, loglevel=logging.DEBUG)
        self.comments = []

    # クライアント接続時に呼ばれる関数
    def new_client(self, client, server):
        print("new client connected and was given id {}".format(client["id"]))

    # クライアント切断時に呼ばれる関数
    def client_left(self, client, server):
        print("client({}) disconnected".format(client["id"]))

    # クライアントからメッセージを受信したときに呼ばれる関数
    def message_received(self, client, server, message):
        message = json.loads(message)
        if len(message) == 0:
            return
        if len(self.comments) != len(message):
            print("comments updated")
            print("client({}) said: {}".format(client["id"], message))
            new_comments = message[: len(message) - len(self.comments)]
            self.server.send_message_to_all(json.dumps(new_comments))
            self.comments = message
        # 全クライアントにメッセージを送信

    # サーバーを起動する
    def run(self):
        # クライアント接続時のコールバック関数にself.new_client関数をセット
        self.server.set_fn_new_client(self.new_client)
        # クライアント切断時のコールバック関数にself.client_left関数をセット
        self.server.set_fn_client_left(self.client_left)
        # メッセージ受信時のコールバック関数にself.message_received関数をセット
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()


if __name__ == "__main__":
    IP_ADDR = "127.0.0.1"  # IPアドレスを指定
    PORT = 9001  # ポートを指定
    ws_server = Websocket_Server(IP_ADDR, PORT)
    ws_server.run()
