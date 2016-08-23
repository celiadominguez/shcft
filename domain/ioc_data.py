
class Indicator:
    """ IocObject class represents a file with indicators of compromise data

     Attributes:
        format: A string representing the IOC file format.
        id: The indicator identification.
      """

    def __init__(self, id, format):
        """ Create a new ioc object """
        self.id = id
        self.format = format

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        self._operator = value

    @property
    def evidences(self):
        return self._evidences

    @evidences.setter
    def evidences(self, value):
        self._evidences = value

    @property
    def indicator(self):
        return self._indicator

    @indicator.setter
    def indicator(self, value):
        self._indicator = value


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

    def __init__(self):
        pass

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, value):
        self._condition = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

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
