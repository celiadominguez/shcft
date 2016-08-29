
from logger import Logger
from recovery.base_recovery import IOCRecovery

@IOCRecovery.register
class DummyRecovery(IOCRecovery):
    def recoverIOC(self, data_path):
        logger = Logger()
        logger.info("DummyRecovery.recoverIOC")