import requests
from lxml import html

def get_html_tree(url):
    try:
        x = requests.get(url)
        tree = html.fromstring(x.content)
        return tree
    except Exception as e:
        print(url)
        raise (e)