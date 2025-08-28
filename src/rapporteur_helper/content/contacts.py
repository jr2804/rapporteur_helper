import copy
from docx.document import Document

from ..word_docx.paragraph import replace
from ..word_docx.tables import replace_in_table


def insert_contacts(document: Document, questionInfo):
    numContacts = len(questionInfo["rapporteurs"])

    # Fid the contact table
    contactTable = None
    for table in document.tables:
        for idx, row in enumerate(table.rows):
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if contactTable != None:
                        break
                    if paragraph.text == "Contact:":
                        contactTable = table

    # Add contacts row if necessary (there are two in the template)
    for i in range(0, numContacts - 2, 1):
        contactTable.rows[-1]._tr.addnext(copy.deepcopy(contactTable.rows[-1]._tr))

    if numContacts == 1:
        contactTable._tbl.remove(contactTable.rows[-1]._tr)

    # Update the contact table
    for contact in questionInfo["rapporteurs"]:
        replace_in_table(contactTable, "Name", f"{contact['firstName']} {contact['lastName']}")
        replace_in_table(contactTable, "Organization", f"{contact['company']}")
        replace_in_table(contactTable, "Country", f"{contact['country']}")
        if "tel" in contact:
            replace_in_table(contactTable, "Tel:\t+xx", f"Tel:\t{contact['tel']}")
        else:
            replace_in_table(contactTable, "Tel:\t+xx", "")
        replace_in_table(contactTable, "a@b.com", f"{contact['email']}")

    # Format text for Section 1:
    target = (
        "the [co-] chairmanship of name of Rapporteur (organization, country) [with the assistance of name of associate Rapporteur (organization, country)]"
    )

    if numContacts == 1:
        text = f"the chairmanship of {contact['firstName']} {contact['lastName']} ({contact['company']}, {contact['country']})"
    else:
        hasAssociate = False
        for contact in questionInfo["rapporteurs"]:
            if "Associate" in contact["role"]:
                hasAssociate = True

        if hasAssociate == False:
            text = "the co-chairmanship of "
            tmp = []
            for contact in questionInfo["rapporteurs"]:
                tmp.append(f"{contact['firstName']} {contact['lastName']} ({contact['company']}, {contact['country']})")
            text += " and ".join(tmp)
        else:
            text = "the chairmanship of "
            for contact in questionInfo["rapporteurs"]:
                if "Rapporteur" in contact["role"]:
                    text += f"{contact['firstName']} {contact['lastName']} ({contact['company']}, {contact['country']})"

            for contact in questionInfo["rapporteurs"]:
                if "Associate" in contact["role"]:
                    text += f" with the assistance of {contact['firstName']} {contact['lastName']} ({contact['company']}, {contact['country']})"

    replace(document, target, text)

if __name__ == "__main__":
    pass
