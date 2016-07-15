

class SHCFTError(Exception):
    def __init__(self, message):
        super(SHCFTError, self).__init__(message)
        self.message = message
pass


class MissingDataPath(SHCFTError):
    pass

class InvalidDataPath(SHCFTError):
    pass