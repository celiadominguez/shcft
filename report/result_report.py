
from reportlab.platypus import (SimpleDocTemplate, PageTemplate,Frame, Table, TableStyle, PageBreak, Spacer, Paragraph)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate,
                                NextPageTemplate, PageBreak, Frame, FrameBreak, Flowable, Paragraph,
                                Image, Spacer)
from reportlab.lib.enums import (TA_CENTER, TA_LEFT)

DEFAULT_REPORT_NAME = "shcft_result.pdf"
LOGO_FILE = "./report/logo.jpg"

TITLE_MSG = "SHERLOCK HOLMES COMPUTER FORENSICS TOOL"
SUBTITLE_MSG = "Informe de resultados del análisis"
SUMMARY_MSG = "Detalles básicos del análisis"
ANALISYS_DATE_MSG = "Fecha del análisis: {:%Y-%m-%d}"
START_TIME_MSG = "Hora de inicio: {:%H:%M}"
END_TIME_MSG = "Hora de finalización: {:%H:%M}"
TOTAL_IOC_MSG = "IOCs analizados: {:d}"
FINAL_STATUS_MSG = "Resultado del análisis: {}"
RESULTS_MSG = "Resultados del análisis"
RESULT_DESC_MSG = "Indicadores de compromiso detectados durante el proceso de análisis."
PAGE_MSG = "Página {:d}"

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
        canvas.drawString(inch, 0.75 * inch, PAGE_MSG.format(doc.page) )
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
        analisysDateTxt.textLines(ANALISYS_DATE_MSG.format(self.results.startTime.date()))
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
        totalIOCTxt.textLines(TOTAL_IOC_MSG.format( self.results.totalIocCount ))
        canvas.drawText(totalIOCTxt)

        # Final Status
        finalStatusTxt = canvas.beginText()
        finalStatusTxt.setTextOrigin(60, 585)
        finalStatusTxt.setFont('Times-Roman', 10)
        finalStatusTxt.textLines(FINAL_STATUS_MSG.format( self.results.status.value) )
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
                             frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, 425)],
                             onPage=doc.summary, onPageEnd=doc.footer),

                PageTemplate(id='content',
                             frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)],
                             onPage=doc.header, onPageEnd=doc.footer),

            ]
        )

        estiloHoja = getSampleStyleSheet()

        # Estilos de la tabla para cabeceras y datos
        thead = estiloHoja["BodyText"]
        thead.fontSize = 7

        table_data = [ ['INDICADOR DE COMPROMISO', 'FORMATO', 'TIPO DE EVIDENCIA', 'VALOR', 'PRUEBA'] ]
        for incident in results.incidents:
            for evidence in incident.evidences:
                table_data.append([Paragraph(self.__prettyPrint__(incident.indicator.id),thead),
                                   Paragraph(self.__prettyPrint__(incident.indicator.format.value),thead),
                                   Paragraph(self.__prettyPrint__(evidence.context),thead),
                                   Paragraph(self.__prettyPrint__(evidence.value),thead),
                                   Paragraph(self.__prettyPrint__(evidence.proof),thead)])

        table_report=[]
        table_report.append(NextPageTemplate('summary'))
        table_report.append(NextPageTemplate('content'))
        table_report.append(Table(table_data, colWidths=[120, 50, 75, 120, 180],
                              style=TableStyle([
                                  ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                                  ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                  ('SIZE', (0, 0), (-1, -1), 7),
                                  ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                  ('BOX', (0, 0), (-1, -1), 1, colors.black),
                                  ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
                              ])
                              )
                            )

        doc.build(table_report)

    def __prettyPrint__(self, text):
        result = ""
        if text is not None:
            if isinstance(text, list):
                for item in text:
                    result += str(item).replace('\n','<br />\n')
            elif isinstance(text, dict):
                for key in text.keys():
                    result.join(text[key].strip())
            else:
                result = text.strip()
        return result
    pass

