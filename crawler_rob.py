######################################################
# extracts all (valid) pictures of given web page
# over multiple pages
######################################################

# import libraries  
import requests
import bs4 as bs
import urllib.request
import re

# specify web page to be crawled via pop up entry
#url = str(input('URL: '))

# hard coded
url = 'https://www.immowelt.de/liste/muenchen/wohnungen/mieten?lat=48.1432&lon=11.55661&sr=50&sort=distance'

# to do detect how many pages
# for now try until fail
for i in range(2):

    # build url to access one page after another
    if i != 0:
        url = url + '&cp=' + str(i+1)

    print(url)

    # initial webcrawler stuff
    opener = urllib.request.build_opener()
    opener.add_headers = [{'User-Agent': 'Mozilla'}]
    urllib.request.install_opener(opener)
    raw = requests.get(url).text
    soup = bs.BeautifulSoup(raw, 'html.parser')

    # find all divs in html of respective page
    rel_div = soup.find_all(lambda tag: tag.name == 'div')

    # oid contains id (=link) of all adds on main page
    oid = []

    for div in rel_div:
        if div.get('data-oid') != None : 
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
