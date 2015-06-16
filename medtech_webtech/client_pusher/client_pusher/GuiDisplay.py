class GuiDisplay(object):
    def __init__(self):
        self.txt = None

    def set_everything_fine(self):
        if self.txt:
            print "Everything is fine"
            self.txt = None

    def set_warning(self, txt):
        if self.txt != txt:
            print "Warning: " + txt
            self.txt = txt

