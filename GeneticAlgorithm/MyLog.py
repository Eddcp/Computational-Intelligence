
class LogMessage(object):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        args = (i() if callable(i) else i for i in self.args)
        kwargs = dict((k, v() if callable(v) else v) for k, v in self.kwargs.items())

        return self.message.format(*args, **kwargs)

