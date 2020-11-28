import requests
import bs4 as bs
import urllib.request
import yaml
from geopy.geocoders import Nominatim
import math


# load config file
with open('config_crawler.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

    city = data["city"]
    country = data["country"]
    radius = data["radius"]
    immoType = data["immoType"]
    intend = data["intend"]
    bjmi = data["bjmi"]
    bjma = data["bjma"]
    roomi = data["roomi"]
    rooma = data["rooma"]
    wflmi = data["wflmi"]
    wflma = data["wflma"]
    primi = data["primi"]
    prima = data["prima"]


# Build Query String
url = 'https://www.immowelt.de/liste/' + \
    city + '/' + immoType + '/' + intend + '?'

if radius:
    geolocator = Nominatim(user_agent="joreka27")
    city = city
    country = country
    loc = geolocator.geocode(city+',' + country)
    lat = loc.latitude
    lon = loc.longitude
    url = url + 'lat=' + str(lat) + '&lon=' + str(lon) + '&sr=' + str(radius)

if bjmi:
    url = url + '&bjmi=' + bjmi

if bjma:
    url = url + '&bjma=' + bjma

if roomi:
    url = url + '&roomi=' + roomi

if rooma:
    url = url + '&rooma=' + rooma

if wflmi:
    url = url + '&wflmi=' + wflmi

if wflma:
    url = url + '&wflma=' + wflma

if primi:
    url = url + '&primi=' + primi

if prima:
    url = url + '&prima=' + prima

url = url + '&sort=distance'

print(url)


# driver = webdriver.PhantomJS()
# driver.get(url)

# lastHeight = driver.execute_script("return document.body.scrollHeight")

# pause = 0.5
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(pause)
#     newHeight = driver.execute_script("return document.body.scrollHeight")
#     if newHeight == lastHeight:
#         break
#     lastHeight = newHeight

# html = driver.page_source
# soup = BeautifulSoup(html, "html5lib")

opener = urllib.request.build_opener()
opener.add_headers = [{'User-Agent': 'Mozilla'}]
urllib.request.install_opener(opener)

rawMain = requests.get(url).text
soup = bs.BeautifulSoup(rawMain, 'html.parser')

# ********************************
#   Get Number of search results
scripts = soup.find_all('script')

for script in scripts:
    if 'utag_data' in str(script):
        utag_data = str(script).split('var utag_data = ')
        J2 = utag_data[1].split('"search_results":')
        J3 = J2[1].split(',')
        search_result = int(J3[0])

print('Suchergebnis :' + str(search_result))


cps = math.floor(search_result / 20)
print("Seiten: " + str(cps))


result = input("Bilder runterladen?")

if result == 'J':

    for i in range(cps):

        # build url to access one page after another
        if i != 0:
            url = url + '&cp=' + str(i+1)

        opener = urllib.request.build_opener()
        opener.add_headers = [{'User-Agent': 'Mozilla'}]
        urllib.request.install_opener(opener)
        raw = requests.get(url).text
        soup = bs.BeautifulSoup(raw, 'html.parser')
        # driver.get(url)
        # html = driver.page_source
        # html = driver.page_source
        # soup = BeautifulSoup(url, "html5lib")

        # find all divs in html of respective page
        rel_div = soup.find_all(lambda tag: tag.name == 'div')

        # oid contains id (=link) of all adds on main page
        oid = []

        for div in rel_div:
            if div.get('data-oid') != None:
                oid.append(div.get('data-oid'))

        url_subs = []

        # build url for every add 8=subpage)
        for i in range(len(oid)):
            url_subs.append('https://www.immowelt.de/expose/' + oid[i])

        print(url_subs)

        for u in url_subs:

            # crawl images on sub pages

            # initial webcrawler stuff
            opener = urllib.request.build_opener()
            opener.add_headers = [{'User-Agent': 'Mozilla'}]
            urllib.request.install_opener(opener)
            raw = requests.get(u).text
            soup = bs.BeautifulSoup(raw, 'html.parser')

            # driver.get(url)
            # html = driver.page_source
            # html = driver.page_source
            # soup = BeautifulSoup(url, "html5lib")

            # identify relevant section for picture content in html
            metas = soup.find_all('meta')

            links = []

            for meta in metas:

                prop = meta.get('property')
                content = meta.get('content')

                if str(prop) == 'og:image':

                    # only real pictures (no logos)
                    if str(content)[0:5] == 'https':
                        links.append(str(content))
                    else:
                        print('no valid picture')

            print('Anzahl Bilder auf Seite: ' + str(len(links)))

            for i in range(len(links)):
                # save files as image to local drive
                filename = 'data\\out\\img_' + u[-7:] + '_' + str(i) + '.png'
                urllib.request.urlretrieve(links[i], filename)
else:
    print('Ciao')
