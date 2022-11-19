import time


class Message:
    msg = ""

    def __init__(self, string):
        self.msg = string + '\n'

    @staticmethod
    def getTime():
        return '(' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ')'

    @staticmethod
    def format(msg):
        return '<font color="black">' + msg + '</font><br>'

    def __str__(self):
        return self.format(self.getTime() + self.msg)


class Error(Message):

    def __init__(self, string):
        Message.__init__(self, string)

    @staticmethod
    def format(msg):
        return '<font color="red">' + msg + '</font><br>'

    def __str__(self):
        return self.format(self.getTime() + '[ERROR]' + self.msg)


if __name__ == "__main__":
    a = Error("Hello")
    print(a)
