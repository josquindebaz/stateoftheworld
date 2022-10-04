#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrap INSEE to get under poverty line population
"""

import re
from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context  # pylint: disable=protected-access


def get():
    """ Get the number of poor people """

    url = "https://www.insee.fr/fr/statistiques/2408345"

    with  urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    raw_value = soup.find("table").find_all("tr")[3].find_all("td")[-1].string
    cleaned_value = re.sub(r"\D", "", raw_value)

    return cleaned_value


if __name__ == "__main__":
    print("Let's get poverty level")
    print("MPAUVRES: ", get())
