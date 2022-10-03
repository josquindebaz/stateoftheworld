#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
Get the CO2 world level
"""

def get():
    url = "https://www.esrl.noaa.gov/gmd/ccgg/trends/monthly.html"
    request = urlopen(url)
    soup = BeautifulSoup(request, "lxml")
    rawValue = soup.find("table").find_all("td")[1].string
    cleanedValue = re.findall("([\d\.]*) ppm", rawValue)[0]
    
    return cleanedValue

if __name__ == "__main__":
    print("Let's get CO2")
    print("CO2_PPM: ", get())
