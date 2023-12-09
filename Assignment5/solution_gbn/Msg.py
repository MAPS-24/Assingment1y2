class Msg:
    MSG_SIZE = 20

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Msg(data=%s)' % (self.data)