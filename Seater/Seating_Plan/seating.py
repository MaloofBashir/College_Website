import openpyxl
import pandas as pd
import PyPDF2
from docx import Document

dictionary_of_subjects={}

def add_rollnos_to_dict(current_subjects,rollno):
    for subject in current_subjects:
        if subject not in dictionary_of_subjects:
            dictionary_of_subjects[subject]=[]
        dictionary_of_subjects[subject].append(rollno)


def add_to_global_dict(pdf_obj,page_no):
        page1=pdf_obj.pages[page_no].extract_text()
        current_subjects=[]
        

        if page1:
            lines=page1.split('\n')

            for lineno,line in enumerate(lines):

                if lineno==14:
                    rollno=line.split(".")[1]
                        
                if lineno==19:
                        subjects=line.split(" ")[0]
                        subjects=subjects.split("-")
                        current_subjects=subjects
                        add_rollnos_to_dict(current_subjects,rollno)

                        return subjects





def getting_all_subs(file):
        pdf_obj=PyPDF2.PdfReader(file)
        num_pages=len(pdf_obj.pages)
        for pageno in range(num_pages):
                subs_of_current_candidate=add_to_global_dict(pdf_obj,pageno)

#running the code to get all roll no saved into dictionary



