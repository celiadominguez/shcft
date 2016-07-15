

from __future__ import generators
from recovery.base_recovery import IOCRecovery


class IOCRecoveryFactory:
    factories = {}
    def addFactory(id, shapeFactory):
        IOCRecoveryFactory.factories.put[id] = shapeFactory
    addFactory = staticmethod(addFactory)
    # A Template Method:
    def createShape(id):
        registry = IOCRecovery().getRegister()
        return registry.get(id)
    createShape = staticmethod(createShape)


def recoveryFactoryNames():
    types = IOCRecovery.__subclasses__()
    for i in types:
        yield i.__name__