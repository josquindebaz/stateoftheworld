#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrap healthmap to get Ebola outbreaks
"""

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get():
    """ Get Ebola casualty """

    url = "http://healthmap.org/ebola"
    with urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    catch = soup.find(class_="deaths").text
    return re.findall(r"\d+", catch)[0]


if __name__ == "__main__":
    print("Let's get Ebola casualty")
    print("EBOLADEAD: ", get())
