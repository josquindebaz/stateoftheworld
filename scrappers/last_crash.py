#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrap to retrieve last airplane crash
"""

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context  # pylint: disable=protected-access


def get():
    """ Get the last crash """

    url = "https://www.planecrashinfo.com/database.htm"
    with urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    url = list(filter(lambda x: re.search(r"\d{4}\.htm", x),
                      [link.get("href") for link in soup.find_all("a")]))[-1]
    url = f"https://www.planecrashinfo.com{url}"
    with urlopen(url) as request:
        soup = BeautifulSoup(request, "lxml")
    raw_value = list(filter(lambda x: re.search(r"\d{4}", x),
                            [link.get("href") for link in soup.find_all("a")]))[-1]
    exploded_url = url.split("/")
    return f"{exploded_url[0]}//{exploded_url[2]}/{exploded_url[3]}/{raw_value}"


if __name__ == "__main__":
    print("Let's get the crash")
    print("LAST_CRASH: ", get())
