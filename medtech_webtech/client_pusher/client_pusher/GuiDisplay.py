import threading
import tornado.ioloop
import tornado.web

#crap anti pattern will fix...
txt = ''

class WebHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(txt or '')

class GuiDisplay(tornado.web.RequestHandler):
    PORT = 9415

    def __init__(self):
        self.application = tornado.web.Application([
            (r"/message", WebHandler),
        ])
        self.application.listen(self.PORT)

        thread = threading.Thread(target=tornado.ioloop.IOLoop.current().start, args=())
        thread.daemon = True
        thread.start()

    def set_everything_fine(self):
        global txt
        if txt:
            print "Everything is fine"
            txt = None

    def set_warning(self, warning_txt):
        global txt
        if txt != warning_txt:
            print "Warning: " + warning_txt
            txt = warning_txt

if __name__ == "__main__":
    display = GuiDisplay()
    display.set_warning('testing')
    display.set_warning('everything fine')
    while(True):
        pass