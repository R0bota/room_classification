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
urlIni = 'https://www.immowelt.de/liste/' + \
    city + '/' + immoType + '/' + intend + '?'

url = urlIni

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
soupMain = bs.BeautifulSoup(rawMain, 'html.parser')

# ********************************
#   Get Number of search results
scripts = soupMain.find_all('script')

for script in scripts:
    if 'utag_data' in str(script):
        utag_data = str(script).split('var utag_data = ')
        J2 = utag_data[1].split('"search_results":')
        J3 = J2[1].split(',')
        search_result = int(J3[0])

print('Suchergebnis :' + str(search_result))


number_pages = math.floor(search_result / 20)
print("Seiten: " + str(number_pages))


result = input("Bilder runterladen?")

if result == 'J':

    for page in range(number_pages):
        # build url to access one page after another
        if page != 0:
            # not first page
            url = urlIni + '&cp=' + str(page+1)
        print("Main URL: " + url)

        opener = urllib.request.build_opener()
        opener.add_headers = [{'User-Agent': 'Mozilla'}]
        urllib.request.install_opener(opener)
        rawList = requests.get(url).text
        soupList = bs.BeautifulSoup(rawList, 'html.parser')

        # find all divs in html of respective page
        div_List = soupList.find_all(lambda tag: tag.name == 'div')

        # oid contains id (=link) of all adds on main page
        oids = []

        for div in div_List:
            # Go through all divs looking for 'data-oid'
            if div.get('data-oid') != None:
                # oids.append(div.get('data-oid'))
                # build url for every add (=subpage)

                url_sub = 'https://www.immowelt.de/expose/' + \
                    div.get('data-oid')
                print("crawl: " + url_sub)

                # crawl images on sub pages
                rawSub = requests.get(url_sub).text
                soupSub = bs.BeautifulSoup(rawSub, 'html.parser')

                # identify relevant section for picture content in html
                metas = soupSub.find_all('meta')

                links = []
                for meta in metas:

                    prop = meta.get('property')

                    if str(prop) == 'og:image':
                        content = meta.get('content')
                        # only real pictures (no logos)
                        if str(content)[0:5] == 'https':
                            links.append(str(content))
                        else:
                            print('no valid picture')

                print('Anzahl Bilder auf Seite: ' + str(len(links)))

                for i in range(len(links)):
                    # save files as image to local drive
                    filename = 'data\\out\\img_' + \
                        div.get('data-oid') + '_' + str(i) + '.png'
                    urllib.request.urlretrieve(links[i], filename)
else:
    print('Ciao')
