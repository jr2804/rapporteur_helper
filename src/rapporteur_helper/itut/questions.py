import re

from ..html import get_html_tree

def get_questions_details(studyGroup: int, studyPeriodId: int) -> dict:
    info = {}
    url = f"https://www.itu.int/net4/ITU-T/lists/loqr.aspx?Group={studyGroup}&Period={studyPeriodId}"

    tree = get_html_tree(url)

    # Find and parse all rows (<tr>) in the document
    rows = tree.xpath("//tr")

    currentQuestion = -1
    for row in rows:
        # Extract WP number and Question title
        try:
            # Question number and WP
            tmp = row.xpath(".//span[contains(@id,'lblQWP')]/text()")[0]

            try:
                res = re.search(rf"Q(\d+)/{studyGroup}.*WP(\d+)/{studyGroup}", tmp)
                qNum = int(res.group(1))
                wpNum = int(res.group(2))
            except:
                # If it fails, check that it is because there is no WP number
                res = re.search(rf"Q(\d+)/{studyGroup}.*", tmp)
                qNum = int(res.group(1))
                wpNum = -1

            # Question title
            qTitle = row.xpath(".//span[contains(@id,'lblQuestion')]/text()")[0]

            if qNum not in info:
                info[qNum] = dict(rapporteurs=[])

            info[qNum].update(dict(wp=wpNum, title=qTitle))

            currentQuestion = qNum

            # print(info[qNum])
        except Exception as e:
            # print(e)
            pass

        # Extract Rapporteurs contact details
        try:
            tmp = {}
            tmp["firstName"] = row.xpath(".//span[contains(@id,'dtlRappQues_lblFName')]/text()")[0]
            tmp["lastName"] = row.xpath(".//span[contains(@id,'dtlRappQues_lblLName')]/text()")[0].upper()
            tmp["role"] = row.xpath(".//span[contains(@id,'dtlRappQues_lblRole')]/text()")[0]
            tmp["company"] = row.xpath(".//span[contains(@id,'dtlRappQues_lblCompany')]/text()")[0]
            tmp["address"] = " ".join(row.xpath(".//span[contains(@id,'dtlRappQues_lblAddress')]/text()"))
            tmp["country"] = row.xpath(".//span[contains(@id,'dtlRappQues_lblAddress')]/text()")[-1]

            try:
                # Some Rapporteurs do not have a telephone number available
                tmp["tel"] = row.xpath(".//span[contains(@id,'dtlRappQues_telLabel')]/text()")[0]
            except:
                pass
            tmp["email"] = row.xpath(".//a[contains(@id,'dtlRappQues_linkemail')]/text()")[0].replace("[at]", "@")

            info[currentQuestion]["rapporteurs"].append(tmp)
        except Exception as e:
            # traceback.print_exc()
            # print(e)
            pass

    if len(info) < 1:
        raise (Exception(f"get_questions_details - Could not parse question details from {url}"))

    return info
