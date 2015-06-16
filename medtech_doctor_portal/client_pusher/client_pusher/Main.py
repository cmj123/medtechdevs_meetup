#main loop
import time
from client_pusher.GuiDisplay import GuiDisplay

from client_pusher.ServerProxy import ServerProxy

def get_data():
    return None

server_proxy = ServerProxy()
gui_display = GuiDisplay()

def main_loop():
    try:
        data = get_data()
        if data:
            server_proxy.send_data(data)
            gui_display.set_everything_fine()
        else:
            time.sleep(1)

    except BaseException as e:
        gui_display.set_warning(e.message)

main_loop()