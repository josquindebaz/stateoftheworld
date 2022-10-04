#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrap NOAA website to retrieve CO2 world level
"""

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get():
    """ Get the CO2 world level """

    url = "https://www.esrl.noaa.gov/gmd/ccgg/trends/monthly.html"
    with  urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    raw_value = soup.find("table").find_all("td")[1].string
    cleaned_value = re.findall(r"([\d\.]*) ppm", raw_value)[0]

    return cleaned_value


if __name__ == "__main__":
    print("Let's get CO2 level")
    print("CO2_PPM: ", get())
