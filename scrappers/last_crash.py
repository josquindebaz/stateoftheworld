#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrap to retrieve last airplane crash
"""

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get():
    """ Get the last crash """

    url = "http://www.planecrashinfo.com/database.htm"
    with  urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    url = list(filter(lambda x: re.search(r"\d{4}\.htm", x),
                      [link.get("href") for link in soup.find_all("a")]))[-1]
    url = f"http://www.planecrashinfo.com{url}"
    with  urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    raw_value = list(filter(lambda x: re.search(r"\d{4}", x),
                            [link.get("href") for link in soup.find_all("a")]))[-1]
    exploded_url = url.split("/")
    return f"{exploded_url[0]}//{exploded_url[2]}/{exploded_url[3]}/{raw_value}"


if __name__ == "__main__":
    print("Let's get the crash")
    print("LAST_CRASH: ", get())
