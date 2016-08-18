
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4
from domain.iocdata import AnalysisResult
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import time

DEFAULT_REPORT_NAME = "shcft_result.pdf"
LOGO_FILE = "./report/logo.jpg"

TITLE_MSG = "SHERLOCK HOLMES COMPUTER FORENSICS TOOL"
SUBTITLE_MSG = "Informe de resultados del análisis"
SUMMARY_MSG = "Detalles básicos del análisis"
ANALISYS_DATE_MSG = "Fecha del análisis: {0}"
START_TIME_MSG = "Hora de inicio: {0}"
END_TIME_MSG = "Hora de finalización: {0}"
TOTAL_IOC_MSG = "IOCs analizados: {0}"
FINAL_STATUS_MSG = "Resultado del análisis: {0}"
RESULTS_MSG = "Resultados del análisis"
RESULT_DESC_MSG = "Indicadores de compromiso detectados durante el proceso de análisis."

class Report(object):

    def __init__(self, reportName=DEFAULT_REPORT_NAME):
        self.reportName = reportName

    def generateReport(self):
        pass


class PDFReport(Report):

    def generateReport(self, results):

        c = canvas.Canvas(DEFAULT_REPORT_NAME)
        story = []

        # LOGO
        c.drawImage(LOGO_FILE, 50, 720, 70, 70)

        # TITLE
        titleTxt = c.beginText()
        titleTxt.setTextOrigin(150,765)
        titleTxt.setFont('Times-Bold',15)
        titleTxt.textLines(TITLE_MSG)
        c.drawText(titleTxt)

        # SUBTITLE
        subtitleTxt = c.beginText()
        subtitleTxt.setTextOrigin(250, 740)
        subtitleTxt.setFont('Times-Roman', 12)
        subtitleTxt.textLines(SUBTITLE_MSG)
        c.drawText(subtitleTxt)

        # SUMMARY
        summaryTxt = c.beginText()
        summaryTxt.setTextOrigin(50, 670)
        summaryTxt.setFont('Times-Bold', 14)
        summaryTxt.textLines(SUMMARY_MSG)
        c.drawText(summaryTxt)
        c.line(50,665,550,665) # Separator

        # Start date
        analisysDateTxt = c.beginText()
        analisysDateTxt.setTextOrigin(60, 645)
        analisysDateTxt.setFont('Times-Roman', 10)
        analisysDateTxt.textLines(ANALISYS_DATE_MSG.format(results.date))
        c.drawText(analisysDateTxt)

        # Start time
        startTimeTxt = c.beginText()
        startTimeTxt.setTextOrigin(60, 630)
        startTimeTxt.setFont('Times-Roman', 10)
        startTimeTxt.textLines( START_TIME_MSG.format(results.startTime))
        c.drawText(startTimeTxt)

        # End time
        endTimeTxt = c.beginText()
        endTimeTxt.setTextOrigin(60, 615)
        endTimeTxt.setFont('Times-Roman', 10)
        endTimeTxt.textLines( END_TIME_MSG.format( results.endTime))
        c.drawText(endTimeTxt)

        # Total IOCs
        totalIOCTxt = c.beginText()
        totalIOCTxt.setTextOrigin(60, 600)
        totalIOCTxt.setFont('Times-Roman', 10)
        totalIOCTxt.textLines(TOTAL_IOC_MSG.format(results.totalIocCount))
        c.drawText(totalIOCTxt)

        # Final Status
        finalStatusTxt = c.beginText()
        finalStatusTxt.setTextOrigin(60, 585)
        finalStatusTxt.setFont('Times-Roman', 10)
        finalStatusTxt.textLines(FINAL_STATUS_MSG.format( results.status) )
        c.drawText(finalStatusTxt)

        # RESULTS
        resultsTxt = c.beginText()
        resultsTxt.setTextOrigin(50, 550)
        resultsTxt.setFont('Times-Bold', 14)
        resultsTxt.textLines(RESULTS_MSG)
        c.drawText(resultsTxt)
        c.line(50, 545, 550, 545) # Separtor

        # Results description
        resultDescTxt = c.beginText()
        resultDescTxt.setTextOrigin(60, 525)
        resultDescTxt.setFont('Times-Roman', 10)
        resultDescTxt.textLines(RESULT_DESC_MSG)
        c.drawText(resultDescTxt)

        #Pintamos la tabla con sus contenidos

        datos = (
            ('Nombre','Tipo','valor'),
            ('The Scarab attack group','DnsEntryItem','www.service.authorizeddns.net')
        )
        tabla = Table (data = datos,
                        style  = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                       ('BOX',(0,0),(-1,-1),2,colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                       ]

                       )
        story.append(tabla)
        story.append(Spacer(0, 15))

        c.showPage()
        c.save()
    pass

