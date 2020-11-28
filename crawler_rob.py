import requests
import bs4 as bs
import urllib.request
import re


#url = str(input('URL: '))

url1 = 'https://www.immowelt.de/liste/muenchen/wohnungen/mieten?lat=48.1432&lon=11.55661&sr=50&sort=distance'

for i in range(10000):

    if i == 0:
        url = url1
    else:
        url = url1 + '&cp=' + str(i+1)

    print(url)

    opener = urllib.request.build_opener()
    opener.add_headers = [{'User-Agent': 'Mozilla'}]
    urllib.request.install_opener(opener)

    raw = requests.get(url).text
    soup = bs.BeautifulSoup(raw, 'html.parser')

    rel_div = soup.find_all(lambda tag: tag.name == 'div')

    oid = []

    for div in rel_div:
        if div.get('data-oid') != None : 
            oid.append(div.get('data-oid')) 

    url_subs = []

    for i in range(len(oid)):
        url_subs.append('https://www.immowelt.de/expose/' + oid[i])

    print(url_subs)

    for u in url_subs:

        opener = urllib.request.build_opener()
        opener.add_headers = [{'User-Agent': 'Mozilla'}]
        urllib.request.install_opener(opener)

        raw = requests.get(u).text
        soup = bs.BeautifulSoup(raw, 'html.parser')

        metas = soup.find_all('meta')

        links = []

        for meta in metas:

            prop = meta.get('property')
            content = meta.get('content')

            if str(prop) == 'og:image':

                if str(content)[0:5] == 'https':
                    links.append(str(content))
                else:
                    print('no valid picture')

        print('Anzahl Bilder auf Seite: ' + str(len(links)))

        for i in range(len(links)):
            filename = 'data\\out\\img_' + u[-7:] + '_' + str(i) + '.png'
            urllib.request.urlretrieve(links[i], filename)
