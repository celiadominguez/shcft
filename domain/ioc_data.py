from enum import Enum


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
        self._evidences = None
        self._description = None
        self._operator = None
        self._children = None
        self._parent = None

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
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

class Evidence:

    def __init__(self):
        self._id = None
        self._type = None
        self._condition = None
        self._content = None
        self._value = None
        self._value = None
        self._compromised = False
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

    @property
    def compromised(self):
        return self._compromised

    @compromised.setter
    def compromised(self, compromised):
        self._compromised = compromised

pass


class Incident:
    def __init__(self, indicator, evidences):
        self.indicator = indicator
        self.evidences = evidences

class AnalysisResult(object):

    class Status(Enum):
        SUCCESS = "SUCESS"
        DETECTED_VULNERABILITIES = "DETECTED VULNERABILITIES"
        pass

    def __init__(self, startTime=None):
        self._startTime = startTime
        self._endTime = None
        self._totalIocCount = None
        self._status = None
        self._incidents = []
        self._platforms = None
        pass

    @property
    def startTime(self):
        return self._startTime

    @startTime.setter
    def startTime(self, value):
        self._startTime = value

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
    def incidents(self):
        return self._incidents

    @incidents.setter
    def incidents(self, incidents):
        self._incidents = incidents

    @property
    def platforms(self):
        return self._platforms

    @platforms.setter
    def platforms(self, value):
        self._platforms = value


pass
