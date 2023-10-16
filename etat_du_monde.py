# -*- encoding: iso-8859-1 -*-
import re
import urllib
import time
import datetime
#import urllib2
import zipfile
import string
import sys

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
requests.packages.urllib3.disable_warnings()

from credentials import atmoKey 
from credentials import openWeatherKey


"""
    test only the indicators in arguments if any
"""

if len(sys.argv) == 1:
    spe = 0
    verbose = 0
else:
    spe = sys.argv[1:]
    verbose = 1


"""
    begin
"""

if verbose:
    print("searching for ", spe)

today = datetime.date.today()

def code_html(text):
    text = re.sub("&uuml;", "ü", text)
    text = re.sub("&eacute;", "é", text)
    text = re.sub("&ouml;", "ö", text)
    text = re.sub("&auml;", "ä", text)
    text = re.sub("&ccedil;", "ç", text)
    text = re.sub("&egrave;", "è", text)
    text = re.sub("(\d) (\d)", "\\1\\2", text)
    return text+ "\n"

"""
description, indicator, url, motif split garde après , motif à chercher avec () pour ce qui est à récupérer
"""
list_type_1 = [
    [u"la température à Paris", 
        "TEMP_PARIS", 
        "http://api.openweathermap.org/data/2.5/weather?id=2988507&appid=%s&units=metric"%openWeatherKey,
        '', 
        '"temp":(-*\d*\.*\d*),'],
    ["le prix du baril", 
        "BARIL", 
        "http://data.cnbc.com/quotes/@CL.1",  
        "",
        '"last":"(\d*\.\d*)"'], 
    ["l'esperance de vie en France", 
        "ESP_VIE_EN_FR", 
        "http://api.worldbank.org/v2/countries/FRA/indicators/SP.DYN.LE00.IN?per_page=3&date=%d:%d&format=json" % ((today.year-5), today.year),
        "", 
        '"value":(\d*\.\d{2})\d*,'],
    ["les visiteurs du site prosperologie",
        "PROSPEROLOGIE",
        "http://prosperologie.org/awstats/awstats.pl?config=prosperologie&framename=mainright",
        "",
        "Viewed traffic&nbsp;\*</td><td><b>([\d,]*)</b>"],
    ["le nombre de chomeur de categorie A",
        "CHOM_CAT_A",
        "http://statistiques.pole-emploi.org/stmt/trsl?fa=M&fb=a&pp=las",
        "",
        '<td width="110" class="white" data-sort-value=(\d*)>'],
]

for item in list_type_1:
    if spe == 0 or item[1] in spe:
        aim = item[0]
        if verbose:
            print(aim)
        try:
            page = urllib.urlopen(item[2]).read()
            if item[3] == "":
                indicator = re.search(item[4], page).group(1)
            else:
                part = re.split(item[3], page)[1]
                indicator = re.search(item[4], part, re.MULTILINE).group(1)
            if verbose: 
                print(item[1], indicator)
        except: 
            print("Failed to retrieve %s" % aim)

"""
description, indicator, url, motif a chercher avec () pour ce qui est a recuperer, no d'occurence a garder,casse
"""
list_type_2 = [
    ["le taux de change du dollar",
        "DOLLAR",
        'https://www.boursorama.com/bourse/devises/taux-de-change-euro-dollar-EUR-USD/',
        "data-ist-last>([\d\.]*)</span><span",
        -1,
        0],
    ["le prime minister","PRIME_MINISTER","https://www.cia.gov/the-world-factbook/countries/united-kingdom/","Prime Minister ([A-z]\w* [A-z]\w*)",0,"cap"],
    ["Bundeskanzler, le chancellier allemand", "BUNDESKANZLER","https://www.cia.gov/the-world-factbook/countries/germany/","Chancellor ([A-z]\w* [A-z]\w*)",0,"cap"],
    ["le nombre de soldats occidentaux tues en Afghanistan","AFGHAN_DEATH_TOLL","http://icasualties.org/App/AfghanFatalities","<p> Afghanistan Fatalities Total: (\d*) </p>", 0, 0],
    ]

for item in list_type_2:
    if spe == 0 or item[1] in spe:
        aim = item[0]
        if verbose:
            print(aim)
        try:
            page = urllib.urlopen(item[2]).read()
            if verbose:
                print("download ok")
            indicator = re.findall(item[3],page)
            if verbose:
                print(indicator)
            indicator = indicator[item[4]]
            if verbose:
                print(indicator)
            if item[5] == "cap":
                try :
                    indicator = string.capwords(indicator)
                except :
                    pass
                if verbose: 
                    print(indicator)
        except :
            print("Failed to retrieve %s" % aim)

if spe == 0 or "GSL" in spe or "SP98" in spe:
    aim = "gas prices"
    if verbose:
        print(aim)
    try :
        url = "http://donnees.roulez-eco.fr/opendata/jour"
        if verbose: 
            print("connecting", url)
        F, N =  urllib.urlretrieve(url)
        Fz = zipfile.ZipFile(F,'r')
        f = Fz.open(Fz.namelist()[0])
        b = f.read()

        paris = re.split('<pdv id="750.[^0]', b)
        if verbose:
            print(len(paris))
        c = 1
        GSL = 0
        SP = 0
        while (GSL == 0 and SP == 0 and c < len(paris)):
            if verbose:
                print(c, paris[c])
            if GSL == 0 :
                testGSL = re.compile("Gazole.*valeur=\"(\d*)")
                if testGSL.search(paris[c]):
                    GSL = testGSL.search(paris[c]).group(1)
                    GSL = str(float(GSL)/ 1000)
                    #maj("GSL" , GSL )
            if SP == 0:
                testSP = re.compile("SP98.*valeur=\"(\d*)")
                if testSP.search(paris[c]):
                    SP = testSP.search(paris[c]).group(1)
                    SP = str(float(SP) /1000)
            c += 1
        if verbose:
            print(GSL, SP)
    except :
        print("Failed to retrieve %s" % aim)

if spe == 0 or "CONCERTATION" in spe or "SOCIOARGU" in spe:
    aim = "socioargu and concertation visitors"
    if verbose :
        print(aim)
    try: 
        headers = { 'User-Agent': 'Python urllib2' }
        req = urllib2.Request("https://logs.openedition.org", None, headers)
        if verbose: 
            print(req)
        page = urllib2.urlopen(req)
        if verbose: 
            print(page)
        pageb = page.read()
        l = ["socioargu", "concertation"]
        for bl in l:
            val = re.findall(".*%s.*</a><td>([\d ]*)<td>"%bl, pageb)
            if verbose:
                print(bl.upper(), val[0])
    except:
        print("Failed to retrieve %s" % aim)

if spe == 0 or "POPU_MONDE" in spe:
    aim = "world population"
    if verbose:
        print(aim)
    try :
        url = "http://www.populationmondiale.com"
        req = urllib2.Request(url, None, {'User-Agent': 'Mozilla/5.0'})
        page = urllib2.urlopen(req).read()
        value = re.sub("[^\d]", "", 
                re.search(r"([\d ]*) personnes", page).group(0))
        if verbose: 
            print(value)
    except :
        print("Failed to retrieve %s" % aim)


if spe == 0 or "BAG_KG" in spe:
    aim = "baguette price"
    if verbose:
        print(aim)
    try :
        r = requests.get("https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/000442423?lastNObservations=1")
        BAG_KG = re.findall('OBS_VALUE="([\d\.]*)"', r.text)[0]
        if verbose:
            print(BAG_KG)
    except :
        print("Failed to retrieve %s" % aim)

if spe == 0 or "POPU_FRA" in spe:
    aim = "French population"
    if verbose: 
        print(aim)
    try:
        r = requests.get("https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/001641586?lastNObservations=1")
        POPU_FRA = re.findall('OBS_VALUE="([\d\.]*)"', r.text)[0]
        if verbose: 
            print(POPU_FRA)
    except :
        print("Failed to retrieve %s" % aim)

if spe == 0 or "CAC40" in spe:
    aim = "CAC 40"
    if verbose: 
        print(aim)
    try:
        page = urllib.urlopen("https://investir.lesechos.fr/cours/historique-indice-cac-40,xpar,px1,fr0003500008,isin.html").read()
        CAC40 = re.findall('<meta instrumentprop="price" content="(.*)"', page)[0]
        if verbose: 
            print(CAC40)
    except:
        print("Failed to retrieve %s" % aim)


if spe == 0 or "SERIE" in spe:
    aim = "popular series"
    if verbose:
        print(aim)
    try:
        page = urllib.urlopen("http://www.allocine.fr/series/meilleures/decennie-2010/annee-2019/").read()
        data_serie = re.findall('thumbnail-link" title="(.*)"', page)
        SERIE = data_serie[0]
        if verbose:
            print(SERIE)
    except :
        print("Failed to retrieve %s" % aim)


if spe == 0 or "ATMO" in spe:
    aim = "AirParif ATMO indicator"
    if verbose:
        print(aim)
    try:
        url = 'https://api.airparif.asso.fr/indices/prevision/commune?insee=75104'
        headers = {"Accept": "application/json",
                'X-Api-Key': atmoKey}
        req = requests.get(url, headers=headers, verify=False)
        res = req.json()
        val = res['75104'][1]["indice"]
        if verbose:
            print([req, res, val]) 
    except :
        print("Failed to retrieve %s" % aim)

if spe == 0 or "COVID" in spe:
    aim = "COVID casualties"
    if verbose:
        print(aim)
    try:
        url = "https://www.worldometers.info/coronavirus/index.php"
        req = urllib2.Request(url, None, { 'User-Agent' : 'Mozilla/5.0' })
        page = urllib2.urlopen(req).read()
        rwolrd = ">World</td>\n<td>[\d\,]*</td>\n<td>[+\d\,]*</td>\n<td>([\d\,]*)</td>"
        world = re.findall(rwolrd, page)[0]
        rfrance = 'France</a></td>\n<td style="font-weight: bold; text-align:right">[\d\,]*</td>\n<td style="font-weight: bold; text-align:right;"></td>\n<td style="font-weight: bold; text-align:right;">([\d\, ]*)</td>'
        france = re.findall(rfrance, page)[0]
        
        if verbose:
            print(world, france)
    except :
        print("Failed to retrieve %s" % aim)


