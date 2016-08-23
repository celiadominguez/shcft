
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle)
from reportlab.lib import colors
#Librerias reportlab a usar:
from reportlab.platypus import (BaseDocTemplate, PageTemplate,
NextPageTemplate, PageBreak, Frame, FrameBreak, Flowable, Paragraph,
Image, Spacer)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
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


class IOCDocTemplate(SimpleDocTemplate):

    def __init__(self, filename, **kw):
        """create a document template bound to a filename (see class documentation for keyword arguments)"""
        if "results" in kw:
            self.results = kw["results"]
            kw.pop("results")
            super(IOCDocTemplate, self).__init__(filename, **kw)
        else:
           raise ValueError("Invalid argument results")

    pass

    def header(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, A4[1] - 50, TITLE_MSG)
        canvas.line(inch, A4[1] - 60, A4[0] - 65, A4[1] - 60)
        canvas.restoreState()

    def footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "Página %d" % doc.page)
        canvas.restoreState()

    def summary(self, canvas, doc):
        canvas.saveState()

        # LOGO
        canvas.drawImage(LOGO_FILE, 50, 720, 70, 70)

        # TITLE
        titleTxt = canvas.beginText()
        titleTxt.setTextOrigin(150, 765)
        titleTxt.setFont('Times-Bold', 15)
        titleTxt.textLines(TITLE_MSG)
        canvas.drawText(titleTxt)

        # SUBTITLE
        subtitleTxt = canvas.beginText()
        subtitleTxt.setTextOrigin(250, 740)
        subtitleTxt.setFont('Times-Roman', 12)
        subtitleTxt.textLines(SUBTITLE_MSG)
        canvas.drawText(subtitleTxt)

        # SUMMARY
        summaryTxt = canvas.beginText()
        summaryTxt.setTextOrigin(50, 670)
        summaryTxt.setFont('Times-Bold', 14)
        summaryTxt.textLines(SUMMARY_MSG)
        canvas.drawText(summaryTxt)
        canvas.line(50, 665, 550, 665)  # Separator

        # Start date
        analisysDateTxt = canvas.beginText()
        analisysDateTxt.setTextOrigin(60, 645)
        analisysDateTxt.setFont('Times-Roman', 10)
        analisysDateTxt.textLines(ANALISYS_DATE_MSG.format(self.results.date))
        canvas.drawText(analisysDateTxt)

        # Start time
        startTimeTxt = canvas.beginText()
        startTimeTxt.setTextOrigin(60, 630)
        startTimeTxt.setFont('Times-Roman', 10)
        startTimeTxt.textLines( START_TIME_MSG.format(self.results.startTime))
        canvas.drawText(startTimeTxt)

        # End time
        endTimeTxt = canvas.beginText()
        endTimeTxt.setTextOrigin(60, 615)
        endTimeTxt.setFont('Times-Roman', 10)
        endTimeTxt.textLines( END_TIME_MSG.format( self.results.endTime))
        canvas.drawText(endTimeTxt)

        # Total IOCs
        totalIOCTxt = canvas.beginText()
        totalIOCTxt.setTextOrigin(60, 600)
        totalIOCTxt.setFont('Times-Roman', 10)
        totalIOCTxt.textLines(TOTAL_IOC_MSG.format(self.results.totalIocCount))
        canvas.drawText(totalIOCTxt)

        # Final Status
        finalStatusTxt = canvas.beginText()
        finalStatusTxt.setTextOrigin(60, 585)
        finalStatusTxt.setFont('Times-Roman', 10)
        finalStatusTxt.textLines(FINAL_STATUS_MSG.format( self.results.status) )
        canvas.drawText(finalStatusTxt)

        # RESULTS
        resultsTxt = canvas.beginText()
        resultsTxt.setTextOrigin(50, 550)
        resultsTxt.setFont('Times-Bold', 14)
        resultsTxt.textLines(RESULTS_MSG)
        canvas.drawText(resultsTxt)
        canvas.line(50, 545, 550, 545)  # Separtor

        # Results description
        resultDescTxt = canvas.beginText()
        resultDescTxt.setTextOrigin(60, 525)
        resultDescTxt.setFont('Times-Roman', 10)
        resultDescTxt.textLines(RESULT_DESC_MSG)
        canvas.drawText(resultDescTxt)
pass

class PDFReport(Report):

    def generateReport(self, results):

        #Pintamos la tabla con sus contenidos
        doc = IOCDocTemplate(DEFAULT_REPORT_NAME, pagesize=A4, results=results)

        doc.addPageTemplates(
            [
                PageTemplate(id='summary',
                             frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, 200)],
                             onPage=doc.summary, onPageEnd=doc.footer),

                PageTemplate(id='content',
                             frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)],
                             onPageEnd=doc.footer, onPage=doc.header),
            ]
        )

        table_data = [Table([
            ['Indicador de Compromiso', 'Tipo de Evidencia', 'Valor'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
            ['The Scarab attack group', 'DnsEntryItem', 'www.service.authorizeddns.net'],
        ],
            style=TableStyle([
                ('ALIGN', (1, 1), (2, 2), 'RIGHT'),
                ('VALIGN', (-1, 0), (-1, 0), 'MIDDLE'),
                ('VALIGN', (0, 0), (1, 0), 'TOP'),
            ])
        )
        ]

        doc.build(table_data)
    pass