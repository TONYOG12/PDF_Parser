from PyPDF2 import PdfReader
import logging
import os
import datetime
import json
import re
from logger import setup_logger


#pdf parser class to handle all parsing functions 
class PDFParser:

    def __init__(self, filePath):

        #dictionary to contain metadata
        self.metadata = {}

         #creating a pdf reader object
        self.pdfReader = PdfReader(filePath)

        self.numPages = len(self.pdfReader.pages)

        self.logger = setup_logger('pdf_parser.log')

    def create_techincal_text(self):
        hi = ""

    def create_md(self):
        hi = "#do something"
        

    def extract_metadata(self):

        #metadata = self.pdfReader.metadata

        #def regular expressions
        case_id_regex = r"([A-Z]+\d+/\d+/\d+)"
        court_regex = r"COURT OF ([A-Z\s]+), ([A-Z]+)" 
        judges_regex = r"((?:[A-Z]+\s)+J\.A\.\s\(PRESIDING\)|(?:(?:[A-Z]+\s)+J\.A\.\s))"
        parties_regex = r"((?:PLAINTIFF|DEFENDANT)\(S\):\s([\w\s,\.&\n-]+))"
        counsel_regex = r"((?:PLAINTIFF|DEFENDANT)\(S\)\sCOUNSEL:\s([\w\s,&\n-]+))"
        date_regex = r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s*(?:,)?\s*(\d{4})"
        city_country_regex= r"^[A-Za-z\s]+ - [A-Za-z\s]+$"


        text = ""

        for pageNum in range(self.numPages):
            page = self.pdfReader.pages[pageNum-1]
            text += page.extract_text()

        
        try:

            date_match = re.search(date_regex, text)

            if date_match:
                day = date_match.group(1)
                month = date_match.group(2)
                year = date_match.group(3)


            # Extract case ID
            case_id_match = re.search(case_id_regex, text)
            case_id = {"number": case_id_match.group(1), "type": "SUIT"}
            
            # Extract court information
            court_match = re.search(court_regex, text)
            court = {"name": court_match.group(1).strip(), "location": {"city": court_match.group(2), "country": "GHANA"}}
            
            # Extract judges
            judges_match = re.findall(judges_regex, text)
            judges = [judge[0].strip() for judge in judges_match]
            
            # Extract parties
            parties_match = re.findall(parties_regex, text)
            parties = {}
            for party_match in parties_match:
                party_type = party_match[0].replace("(S)", "")
                parties[party_type] = [party.strip() for party in party_match[1].split(",")]
            
            # Extract counsel
            counsel_match = re.findall(counsel_regex, text)
            counsel = {}
            for counsel_match in counsel_match:
                counsel_type = counsel_match[0].replace("(S)", "")
                counsel[counsel_type] = [c.strip() for c in counsel_match[1].split(",")]

            # Extract plaintiff
            plaintiff = re.search(r'PLAINTIFF\s*/[A-Z]+', text).group().split('/')[-1]

            # Extract defendants
            defendants = re.findall(r'\d+\.\s(.+?)\s*\.{3,}', text)

            presiding_judge = r'^(.*)\s\(PRESIDING\)$'
            match = re.match(presiding_judge, text)
            if match:
                presider = match.group(1)
                print(presider)
            else:
                self.logger.warning("");


            self.metadata = {
            "source": "lawsghana.com",
            "booksReferredTo": [],
            "casesReferredTo": [],
            "caseId": case_id,
            "court": court,
            "counsel": counsel,
            "editorialNote": None,
            "headNotes": None,
            "indices": None,
            "judgement": {
                "date": date_match,
                "year": year,
                "month": month,
                "day": day
            },
            "judges": judges,
            "lawReportsCitations": [],
            "natureOfProceedings": None,
            "mediaNeutralCitation": None,
            "presidingJudge": presiding_judge,
            "partiesOfSuit": {
                "Plaintiff/Appellant": [
                    "AARON KWESI KAITOO"
                ],
                "Defendant/Respondent": [
                    "THE REPUBLIC"
                ]
            },
            "statutesReferredTo": [],
            "title": {
                "long": "".join(plaintiff) + "" + "vs" + "".join(defendants), #Should list all Plaintiffs and Defendants
                "short": f"{plaintiff[0]} vs {defendants[0]}" #Should list only the first Plaintiff and Defendant
            }

            }

        except Exception as e:
            self.logger.error("An error occurred while extracting metadata from file {}: {}".format(self.filePath, str(e)))
            presiding_judge = r'^(.*)\s\(PRESIDING\)$'
            match = re.match(presiding_judge, text)
            if match:
                presiding_judge = match.group(1)
                print(presiding_judge)

            return text

            


        return text





    

       

parser = PDFParser('/home/tony/Documents/Kwame AI intern work/Court Case 2.pdf')

print(parser.extract_metadata())