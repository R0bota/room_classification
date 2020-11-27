import bs4 as bs
import urllib.request
import time
from datetime import datetime
import pandas as pd
import json
import lxml


df = pd.DataFrame()

for seite in range(1,2):
    
    print("Loop " + str(seite) + " startet.")
    
    l=[]

    try:
        
        print("https://www.immobilienscout24.de/Suche/S-2/P-" + str(seite) + "/Wohnung-Kauf")
        soup = bs.BeautifulSoup(urllib.request.urlopen("https://www.immowelt.de/liste/muenchen-altstadt-lehel/wohnungen/mieten?geoid=10809162000017&zip=80333&sort=relevanz").read(), 'lxml')
        print("Aktuelle Seite: "+"https://www.immobilienscout24.de/Suche/S-2/P-" + str(seite) + "/Wohnung-Kauf/archiv")
        
        for paragraph in soup.find_all("a"):

            if r"/expose/" in str(paragraph.get("href")):
                l.append(paragraph.get("href").split("#")[0])

            l = list(set(l))

        for item in l:

            try:

                soup = bs.BeautifulSoup(urllib.request.urlopen('https://www.immobilienscout24.de'+item).read(),'lxml')

                data = pd.DataFrame(json.loads(str(soup.find_all("script")).split("keyValues = ")[1].split("}")[0]+str("}")),index=[str(datetime.now())])

                data["URL"] = str(item)
                print(str(item))
                beschreibung = []
				
				
	
			

                for x in soup.find_all("pre"):
                    beschreibung.append(x.text)
                    
                	

                #data["beschreibung"] = str(beschreibung)
                data["beschreibung"] = str()
                for i in soup.find_all("dd", attrs={"class":"is24qa-heizkosten grid-item three-fifths"}):
                    beschreibung = i.text
                    beschreibung = beschreibung.replace("\n", " ")	
                    beschreibung = beschreibung.replace("\t", " ")		
                    beschreibung = beschreibung.replace(";", " ")		    			
                #data["HK enthalten"] = str(beschreibung)
                data["HK enthalten"] = str()
                beschreibung = ""
                data["obj_street"] = str()
                df = df.append(data)

            except Exception as e: 
                print(str(datetime.now())+": " + str(e))
                l = list(filter(lambda x: x != item, l))
                print("ID " + str(item) + " entfernt.")
     
        
        print("Loop " + str(seite) + " endet.\n")
        
    except Exception as e: 
        print(str(datetime.now())+": " + str(e))

print("FERTIG!")

#df.to_csv("Wohnung_Kauf-" + str( datetime.now())[:19].replace(":","").replace(".","").replace("-",".") + ".csv",sep=";",decimal=",",encoding = "utf-8",index_label="timestamp")  
