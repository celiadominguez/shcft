from datetime import datetime
import time

from domain.ioc_data import AnalysisResult, Incident


class IOCAnalysis():

    @staticmethod
    def analyzeIndicatorsOfCompromise(indicators, results):
        results.totalIocCount = indicators.__len__()
        results.status = AnalysisResult.Status.DETECTED_VULNERABILITIES
        results.endTime = datetime.now()

        # Analyze results
        incidents = []
        for indicator in indicators:

            if isinstance(indicator, list):
                indicator = indicator

            # Recursive validation
            IOCAnalysis.evalueIndicator(indicator, incidents)

        results.incidents = incidents

        pass

    @staticmethod
    def evalueIndicator( indicator, incidents):
        # Validating evidences
        evidences = []
        if indicator.evidences != None:
            for evidence in indicator.evidences:
                evidences.append(evidence)

            # Create incident if exists vunerability evidences
            if evidences.__sizeof__() > 0:
                incident = Incident(indicator, evidences)
                incidents.append(incident)

        if indicator.children != None:
            for child_indicator in indicator.children:
                IOCAnalysis.evalueIndicator(child_indicator, incidents)

        return incidents

pass