from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup as soup
import json
import re

base = "https://www.ptt.cc"
home = "/bbs/Beauty/index.html"
cookies = {"over18": "1"}


def index(request):
    response = requests.get(base + home, cookies=cookies)
    text = response.text
    doc = soup(text, "html.parser")
    main_container = doc.find(id="main-container")
    pages = main_container.find_all("div", class_="title")
    p = []
    for page in pages:
        for a in page.find_all("a"):
            p.append(base + a.get("href"))
    ans = []
    i = 0

    pattern = "https://(i\\.)?imgur\\.com/[a-zA-Z0-9]{7}(\\.jpg)?"

    for url in p:
        for string in getSinglePage(url):
            if re.match(pattern, string):
                ans.append(string)
        ++i
        if i > 1:
            break

    return HttpResponse("[" + ", ".join(ans) + "]")

def getSinglePage(url):
    response = requests.get(url, cookies=cookies)
    doc = soup(response.text, "html.parser")
    content = doc.find("meta", {"name": "description"}).get("content")
    return content.split("\n")
