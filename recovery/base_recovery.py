
class IOCRecovery(object):
    registry = {}
    def register(cls):
        cls.registry[cls.__name__] = cls()  # Instance new subclass
        return cls

    def getRegister(self):
        return self.registry

    pass