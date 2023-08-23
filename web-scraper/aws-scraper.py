import re
import requests
import json
from bs4 import BeautifulSoup

baseurl = 'https://aws.amazon.com/'
with open('/Users/per.aronsson/Documents/AWS/data-mod.json', 'r') as datafile:
  data=datafile.read()

obj = json.loads(data)
categories = obj['categories']
for i, category in enumerate(categories):
  for j, service in enumerate(category['services']):
    obj['categories'][i]['services'][j]['title'] = categories[i]['services'][j]['title'].strip()
    response = requests.get(service['url'])
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    desc = soup.select("#aws-page-content-main > div:has(h2[id=How_it_works]) p")
    if len(desc) == 0:
      desc = soup.select("#aws-page-content-main span.eb-summary p")
    if len(desc) == 0:
      desc = soup.select("#aws-page-content-main h2[id=How_it_works]+div")
    if len(desc) == 0:
      desc = soup.select("#aws-page-content-main h2+div p")
    if len(desc) == 0:
      desc = soup.select("#aws-page-content-main h2+div")
    if len(desc) == 0:
      desc = soup.select("#aws-page-content-main h1")
    if len(desc) > 0:
      trimdesc = desc[0].text.strip(' \t\n\r')
      obj['categories'][i]['services'][j]['description'] = trimdesc
      print(trimdesc, end='\n', flush=True)
    else:
      print('Failed: '+service['url'], end='\n', flush=True)
    #print('*', end='', flush=True)
print('\nFinished', end='\n', flush=True)
jsonString = json.dumps(obj)
jsonFile = open("/Users/per.aronsson/Documents/AWS/data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
