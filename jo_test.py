import requests
import bs4 as bs
import urllib.request

# url = str(input('URL: '))
url = 'https://www.immowelt.de/liste/muenchen-altstadt-lehel/wohnungen/mieten?geoid=10809162000017&prima=900&sort=createdate%2Bdesc'

opener = urllib.request.build_opener()
opener.add_headers = [{'User-Agent': 'Mozilla'}]
urllib.request.install_opener(opener)

rawMain = requests.get(url).text
soup = bs.BeautifulSoup(rawMain, 'html.parser')

# metas = soup.find_all('meta')
div_tags = soup.find_all('div')
oIds = []
for div in div_tags:
    oId = div.get('data-oid')
    if oId is not None:
        print(str(oId))
        oidUrl = 'https://www.immowelt.de/expose/' + str(oId)
        raw = requests.get(oidUrl).text
        soupOid = bs.BeautifulSoup(raw, 'html.parser')
        metas = soupOid.find_all('meta')

        links = []

        for meta in metas:
            prop = meta.get('property')
            content = meta.get('content')
            if str(prop) == 'og:image':
                print('Property: ' + str(content))
                imageUrl = str(content)
                if 'https:' in imageUrl:
                    links.append(str(content))

        print('Anzahl Bilder auf Seite: ' + str(len(links)))

        for i in range(len(links)):
            filenamePart1 = 'data\\out\\' + oId
            filenamePart2 = '_{}.png'.format(i)
            filename = filenamePart1 + filenamePart2
            print(filename)
            urllib.request.urlretrieve(links[i], filename)


# links = []

# for meta in metas:
#     prop = meta.get('property')
#     content = meta.get('content')
#     print('Property: ' + str(prop))
#     if str(prop) == 'og:image':
#         print('Property: ' + str(content))
#         links.append(str(content))

# print('Anzahl Bilder auf Seite: ' + str(len(links)))

# for i in range(len(links)):
#     filename = 'data\\out\\img{}.png'.format(i)
#     urllib.request.urlretrieve(links[i], filename)
#     print('Fertig')
