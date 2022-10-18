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

def code_html(texte):
    texte = re.sub("&uuml;", "ü", texte)
    texte = re.sub("&eacute;", "é", texte)
    texte = re.sub("&ouml;", "ö", texte)
    texte = re.sub("&auml;", "ä", texte)
    texte = re.sub("&ccedil;", "ç", texte)
    texte = re.sub("&egrave;", "è", texte)
    texte = re.sub("(\d) (\d)", "\\1\\2", texte)
    return texte+ "\n"

"""
description, indicateur, url, motif split garde après , motif à chercher avec () pour ce qui est à récupérer
"""
liste_type_1 = [ 
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

for item in liste_type_1:
    if spe == 0 or item[1] in spe:
        if verbose:
            print("Recuperons %s " % item[0])
        try:
            page = urllib.urlopen(item[2]).read()
            if item[3] == "":
                indicateur = re.search(item[4], page).group(1)
            else:
                partie = re.split(item[3], page)[1]
                indicateur = re.search(item[4], partie, re.MULTILINE).group(1)     
            #maj(item[1], indicateur)
            if verbose: 
                print(item[1], indicateur)
        except: 
            print("je n'ai pas pu recuperer %s" % (item[0]))

"""
description, indicateur, url, motif a chercher avec () pour ce qui est a recuperer, no d'occurence a garder,casse
"""
liste_type_2 = [ 
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

for item in liste_type_2:
    if spe == 0 or item[1] in spe:
        if verbose:
            print("Recuperons %s " % item[0])
        try:
            page = urllib.urlopen(item[2]).read()
            if verbose:
                print("telec ok")
            indicateur = re.findall(item[3],page)
            if verbose:
                print(indicateur)
            indicateur = indicateur[item[4]]
            if verbose:
                print(indicateur)
            if item[5] == "cap":
                try :
                    indicateur = string.capwords(indicateur)
                except :
                    pass
                if verbose: print(indicateur)
            #maj(item[1],indicateur)
        except : 
            print( u"je n'ai pas pu recuperer %s" % (item[0]))






if spe == 0 or "GSL" in spe or "SP98" in spe:
    if verbose:
        print("Je recupere le prix de l'essence")
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
                    #maj("SP98" , SP )
            c += 1
        if verbose:
            print(GSL, SP)
    except :
        print("Je n'ai pas pu recuperer le prix de l'essence")

if spe == 0 or "CONCERTATION" in spe or "SOCIOARGU" in spe:
    if verbose : print("Recuperons les visiteurs de socioargu et de concertation")
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
            #maj(bl.upper(), val[0])
            if verbose: 
                print(bl.upper(), val[0])
    except:
        print ("je n'ai pas pu recuperer les visiteurs de socioargu et de concertation")

if spe == 0 or "POPU_MONDE" in spe:
    if verbose: print("Recuperons la population mondiale")
    try :
        url = "http://www.populationmondiale.com"
        req = urllib2.Request(url, None, {'User-Agent': 'Mozilla/5.0'})
        page = urllib2.urlopen(req).read()
        value = re.sub("[^\d]", "", 
                re.search(r"([\d ]*) personnes", page).group(0))
        if verbose: 
            print(value)
        #maj("POPU_MONDE", value)
    except :
        print("je n'ai pas pu recuperer la population mondiale")
	

if spe == 0 or "BAG_KG" in spe:
    if verbose:
        print("Recuperons le prix de la baguette")
    try :
        r = requests.get("https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/000442423?lastNObservations=1")
        BAG_KG = re.findall('OBS_VALUE="([\d\.]*)"', r.text)[0]
        if verbose:
            print(BAG_KG)
        #maj("BAG_KG", BAG_KG)
    except :
        print("je n'ai pas pu recuperer le prix de la baguette")

if spe == 0 or "POPU_FRA" in spe:
    if verbose: 
        print("Recuperons la pop francaise")
    try:
        r = requests.get("https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/001641586?lastNObservations=1")
        POPU_FRA = re.findall('OBS_VALUE="([\d\.]*)"', r.text)[0]
        if verbose: 
            print(POPU_FRA)
        #maj("POPU_FRA", POPU_FRA)
    except :
        print ("je n'ai pas pu recuperer la pop francaise")

if spe == 0 or "CAC40" in spe:
    if verbose: 
        print("Recuperons le CAC 40")
    try:
        page = urllib.urlopen("https://investir.lesechos.fr/cours/historique-indice-cac-40,xpar,px1,fr0003500008,isin.html").read()
        CAC40 = re.findall('<meta instrumentprop="price" content="(.*)"', page)[0]
        if verbose: 
            print(CAC40)
        #maj("CAC40", CAC40)
    except:
        print("je n'ai pas pu recuperer le CAC 40")


if spe == 0 or "SERIE" in spe:
    if verbose:
        print("la serie en vogue")
    try:
        page = urllib.urlopen("http://www.allocine.fr/series/meilleures/decennie-2010/annee-2019/").read()
        data_serie = re.findall('thumbnail-link" title="(.*)"', page)
        SERIE = data_serie[0]
        if verbose:
            print(SERIE)
        #maj("SERIE", SERIE)
    except :
        print("je n'ai pas pu recuperer la serie en vogue")


if spe == 0 or "ATMO" in spe:
    if verbose:
        print("l'indice ATMO de AirParif")
    try:
        url = 'https://api.airparif.asso.fr/indices/prevision/commune?insee=75104'
        headers = {"Accept": "application/json",
                'X-Api-Key': atmoKey}
        req = requests.get(url, headers=headers, verify=False)
        res = req.json()
        val = res['75104'][1]["indice"]
        #maj("ATMO", val)
        if verbose:
            print([req, res, val]) 
    except :
        print ("je n'ai pas pu recuperer ATMO")

if spe == 0 or "COVID" in spe:
    if verbose:
        print("les morts de la COVID")
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
        #maj("MORTSCOVIDMOND", world)
        #maj("MORTSCOVIDFRANCE", france)
    except :
        print("je n'ai pas pu recuperer les donnees du COVID")


