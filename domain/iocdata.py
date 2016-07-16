
class IocObject:
    """ IocObject class represents a file with indicators of compromise data

     Attributes:
        format: A string representing the IOC file format.
        id: The indicator identification.

      """

    def __init__(self, format, id):
        """ Create a new ioc object """
        self.format = format
        self.id = id


class Indicator:
    """ Indicator class represents a indicators of compromise data

         Attributes:
            id: The indicator identification
          """

    def __init__(self, id):
        """ Create a new ioc object """
        self.id = id

class Evidence:

    def __init__(self, id):
        pass
pass



class Result(object):

    def __init__(self, startTime):
        self.startTime = startTime
        self.incidents = 0
        pass

    @property
    def endTime(self):
        return self.endTime

    @endTime.setter
    def endTime(self, value):
        self.endTime = value

    @property
    def totalIocCount(self):
        return self.totalIocCount


    @totalIocCount.setter
    def totalIocCount(self, value):
        self.totalIocCount = value

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, value):
        self.status = value

    @property
    def incidentsByType(self, type):
        return self.incidentsByType[type]

    @status.setter
    def incidentsByType(self, type, incidents):
        self.incidentsByType[type] = incidents

    def increateIncidents(self):
        self.incidents =  self.incidents + 1

    def getIncidents(self):
        return self.incidents
pass
