#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrap to retreive boxoffice star movie
"""

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get():
    """ Get the boxoffice star movie """

    url = "http://www.cine-directors.net/boxoff.htm"
    with  urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    raw_value = soup.find_all("table")[3].find_all("tr")[2].find_all("td")[1].contents[1].string
    cleaned_value = re.sub(r"\s{2,}"," ", raw_value.strip())
    return cleaned_value

if __name__ == "__main__":
    print("Let's get the boxoffice")
    print("BoxOffice: ", get())
