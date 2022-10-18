#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrap wikipedia website to retrieve the last Peace Nobel prize
"""

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get():
    """ Get the last Peace Nobel prize """

    url = "https://fr.wikipedia.org/wiki/Prix_Nobel_de_la_paix"
    with urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    fist_table = soup.find("table")
    trs = fist_table.find_all("tr")
    catch = [tr.find("td").text for tr in trs if re.search("Dernier", tr.text)][0]
    return catch.strip()


if __name__ == "__main__":
    print("Let's get last Peace Nobel prize")
    print("NOBEL_PAIX: ", get())
