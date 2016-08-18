
class Indicator:
    """ IocObject class represents a file with indicators of compromise data

     Attributes:
        format: A string representing the IOC file format.
        id: The indicator identification.

      """

    def __init__(self, id, description, condition, evidences, indicator):
        """ Create a new ioc object """
        self.id = id
        self.description = description
        self.condition = condition
        self.evidences = evidences
        self.indicator = indicator

class Incident:
    """ Indicator class represents a indicators of compromise data

         Attributes:
            id: The indicator identification
          """

    def __init__(self, indicator, evidences):
        """ Create a new ioc object """
        self.indicator = indicator
        self.evidences = evidences

class Evidence:

    def __init__(self, id, type, condition, content, value):
        """ Create a new ioc object """
        self.id = id
        self.type = type
        self.condition = condition
        self.content = content
        self.value = value
pass



class AnalysisResult(object):

    def __init__(self, startTime):
        self.startTime = startTime
        self.incidents = 0
        pass

    @property
    def endTime(self):
        return self._endTime

    @endTime.setter
    def endTime(self, value):
        self._endTime = value

    @property
    def totalIocCount(self):
        return self._totalIocCount


    @totalIocCount.setter
    def totalIocCount(self, value):
        self._totalIocCount = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def incidentsByType(self, type):
        return self._incidentsByType[type]

    @status.setter
    def incidentsByType(self, type, incidents):
        self._incidentsByType[type] = incidents

    @property
    def platforms(self):
        return self._platforms

    @platforms.setter
    def platforms(self, value):
        self._platforms = value

    def increateIncidents(self):
        self.incidents =  self.incidents + 1

    def getIncidents(self):
        return self.incidents

pass
