import os
from pprint import pprint

from docx import Document as open_docx
from docx.document import Document

from . import template_file
from .content.documents import insert_documents
from .content.contacts import insert_contacts
from .word_docx.paragraph import find_element, replace
from .itut.questions import get_questions_details
from .itut.work_programme import get_work_program, insert_work_program


questions = list(range(1, 21))
# questions = [1,2, 7, 14]
# meetingDate = "220607"
add_qall = False

# Update these parameters for each meeting
studyGroup = 12
meetingDetails = "Geneva, 14-23 January 2025"
meetingDate = "250114"

# Update these parameters to the current study period
studyPeriodId = 18
studyPeriodStart = 25
isn_sp = 9677

def main(verbose: bool = True):
    try:
        questionInfo = get_questions_details(studyGroup, studyPeriodId)
        # pprint(questionInfo)
    except Exception as e:
        print("Error - Cannot fetch question details from ITU-T website")
        raise (e)

    for question in questions:
        print(f"\n### Generating report for Q{question}")

        try:
            hostname = "https://www.itu.int"
            endpoints_c = []
            if add_qall:
                endpoints_c += [
                    dict(
                        url=f"{hostname}/md/meetingdoc.asp?lang=en&parent=T{studyPeriodStart}-SG{studyGroup}-{meetingDate}-C&question=QALL/{studyGroup}",
                        prefix=f"SG{studyGroup}-C",
                        title="Contributions",
                    )
                ]
            endpoints_c += [
                dict(
                    url=f"{hostname}/md/meetingdoc.asp?lang=en&parent=T{studyPeriodStart}-SG{studyGroup}-{meetingDate}-C&question=Q{question}/{studyGroup}",
                    prefix=f"SG{studyGroup}-C",
                    title="Contributions",
                ),
            ]

            endpoints_td = []
            if add_qall:
                endpoints_td += [
                    dict(
                        url=f"{hostname}/md/meetingdoc.asp?lang=en&parent=T{studyPeriodStart}-SG{studyGroup}-{meetingDate}-TD&question=QALL/{studyGroup}",
                        prefix=f"SG{studyGroup}-TD",
                        title="Temporary Documents",
                    ),
                ]
            endpoints_td += [
                dict(
                    url=f"{hostname}/md/meetingdoc.asp?lang=en&parent=T{studyPeriodStart}-SG{studyGroup}-{meetingDate}-TD&question=Q{question}/{studyGroup}",
                    prefix=f"SG{studyGroup}-TD",
                    title="Temporary Documents",
                ),
            ]
            # pprint(endpoints)

            with template_file.open("rb") as f:
                document: Document = open_docx(f)

            # for style in document.styles:
            #     print(f"{style.name} {style.type}")

            # Meeting date
            replace(document, "[place, dates]", meetingDetails)

            # Abstract
            abstract = f"This document contains the Status report of Question {question}/{studyGroup}: {questionInfo[question]['title']} for the meeting in {meetingDetails}."
            replace(document, "[Insert an abstract]", abstract)

            # Insert contributions
            if (docSection := find_element(document, "Copy table of contributions")):
                insert_documents(docSection, endpoints_c)

            # Insert temporary documents
            # print("  Inserting temporary documents")
            if (docSection := find_element(document, "Copy the TD table")):
                insert_documents(docSection, endpoints_td)

            # Replace question number
            replace(document, f"X/{studyGroup}", f"{question}/{studyGroup}")
            replace(document, f"t{studyPeriodStart}sg{studyGroup}qX@lists.itu.int", f"t{studyPeriodStart}sg{studyGroup}q{question}@lists.itu.int")

            # Replace working party number
            replace(document, f"Working Party y/{studyGroup}", f"Working Party {questionInfo[question]['wp']}/{studyGroup}")

            # Replace question title
            replace(document, "[title of question]", questionInfo[question]["title"])
            replace(document, "Title of question", questionInfo[question]["title"])

            # Insert contacts
            insert_contacts(document, questionInfo[question])

            # Insert work programme
            workProgram = get_work_program(question)
            # pprint(workProgram)
            insert_work_program(document, workProgram)

            try:
                os.mkdir(f"./{meetingDate}")
            except:
                pass

            document.save(f"./{meetingDate}/Q{question}_status_report.docx")

        except Exception as e:
            pprint(e)
            #traceback.print_stack()
            # pprint(questionInfo)


if __name__ == "__main__":
    main()