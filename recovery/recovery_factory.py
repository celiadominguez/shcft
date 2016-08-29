

from __future__ import generators
from recovery.base_recovery import IOCRecovery


class IOCRecoveryFactory:

    # A Template Method:
    def createRecovery(id):
        registry = IOCRecovery().getRegister()
        return registry.get(id)
    createRecovery = staticmethod(createRecovery)


def recoveryFactoryNames():
    types = IOCRecovery.__subclasses__()
    for i in types:
        yield i.__name__