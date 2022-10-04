#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrap to retrieve box-office star movie
"""

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context  # pylint: disable=protected-access


def get():
    """ Get the box-office star movie """

    url = "https://www.cine-directors.net/boxoff.htm"
    with urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    raw_value = soup.find_all("table")[3].find_all("tr")[2].find_all("td")[1].contents[1].string
    cleaned_value = re.sub(r"\s{2,}", " ", raw_value.strip())
    return cleaned_value


if __name__ == "__main__":
    print("Let's get the box-office")
    print("BoxOffice: ", get())
