import requests
import bs4 as bs
import urllib.request


url = str(input('URL: '))

opener = urllib.request.build_opener()
opener.add_headers = [{'User-Agent': 'Mozilla'}]
urllib.request.install_opener(opener)

raw = requests.get(url).text
soup = bs.BeautifulSoup(raw, 'html.parser')

metas = soup.find_all('meta')

links = []

for meta in metas:
    prop = meta.get('property')
    content = meta.get('content')
    print('Property: ' + str(prop))
    if str(prop) == 'og:image':
        print('Property: ' + str(content))
        links.append(str(content))

print('Anzahl Bilder auf Seite: ' + str(len(links)))

for i in range(len(links)):
    filename = 'data\\out\\img{}.png'.format(i)
    urllib.request.urlretrieve(links[i], filename)
    print('Fertig')


# raw = requests.get(url).text
# soup = bs.BeautifulSoup(raw, 'html.parser')

# imgs = soup.find_all('img')

# links = []

# for img in imgs:
#     link = img.get('src')
#     if 'http://' not in link:
#         link = url + link
#     links.append(link)

# print('Anzahl Bilder auf Seite: ' + str(len(links)))

# for i in range(len(links)):
#     filename = 'data\\out\\img{}.png'.format(i)
#     urllib.request.urlretrieve(links[i], filename)
#     print('Fertig')
