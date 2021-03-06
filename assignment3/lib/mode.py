class Mode:
    def __init__(self, modes, starts=0):
        self.modes = modes
        self.index = starts

    def get(self, index=None, next=False, block=False):
        index = index or self.index
        try:
            return self.modes[index]
        except:
            raise Exception('index out of range')
        finally:
            self.index+=next
            if not block:
                self.index%=len(self.modes)

    def next(self):
        self.index=(self.index+1)%len(self.modes)

    def prev(self):
        self.index=(self.index-1)%len(self.modes)
