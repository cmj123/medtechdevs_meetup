#main loop
import time

from client_pusher.ServerProxy import ServerProxy


def get_data():
    return None

server_proxy = ServerProxy()

def main_loop():
    data = get_data()
    if data:
        server_proxy.send_data(data)
    else:
        time.sleep(1)

main_loop()