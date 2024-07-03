class IBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        pass
