
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm

class Report(object):

    def __init__(self, data, reportName):
        self.data = data
        self.reportName = reportName

    def generateReport(self):
        pass


class PDFReport(Report):

    def generateReport(self, results):
        c = canvas.Canvas(self.reportName)
        c.drawImage('ar.jpg', 0, 0, 10 * cm, 10 * cm)
        c.showPage()
        c.save()
    pass

