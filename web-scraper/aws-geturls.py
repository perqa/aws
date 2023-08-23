import re
import requests
import json
from bs4 import BeautifulSoup

baseurl = 'https://aws.amazon.com/'
with open('/Users/per.aronsson/Documents/AWS/AWS-services-SAA003.txt', 'r') as reader:
  resobj = {'title':'AWS Services', 'categories':[]}
  # Read and print the entire file line by line
  line = 'new'
  while line != '':  # The EOF char is an empty string
    line = reader.readline()
    # Header / Categories
    if line.find(':') > 0:
      resobj['categories'].append({'title': re.sub(r'[^A-Za-z0-9\- ]+', '', line), 'services':[]})
    # AWS Service list item
    else:
      modline = re.sub(r'[^A-Za-z0-9\- ]+', '', line.lower().replace('aws ', '').replace('amazon ', '')).strip().replace(' ','-')
      response = requests.get(baseurl+modline)
      resobj['categories'][-1]['services'].append({'title':re.sub(r'[^A-Za-z0-9\- ]+', '', line), 'status':'N/A', 'url':'N/A'})
      success = False
      if response.status_code == 200:
        success = True
        variant = modline
        resobj['categories'][-1]['services'][-1]['status'] = 'ok'
      else:
        variants = []
        variants.append(modline.split('-')[-1])
        variants.append(modline.split('-')[0])
        variants.append(modline.replace('-', ''))
        for variant in variants:
          response = requests.get(baseurl+variant)
          if response.status_code == 200:
            success = True
            resobj['categories'][-1]['services'][-1]['status'] = 'modified'
            break
      if success:
        resobj['categories'][-1]['services'][-1]['url'] = baseurl+variant
      else:
        resobj['categories'][-1]['services'][-1]['status'] = 'failed'
        resobj['categories'][-1]['services'][-1]['url'] = baseurl+modline
    print('*', end='', flush=True)
  print('\n', end='', flush=True)
print('Finished', end='\n', flush=True)
jsonString = json.dumps(resobj)
jsonFile = open("/Users/per.aronsson/Documents/AWS/data-urls.json", "w")
jsonFile.write(jsonString)
jsonFile.close()



#html = requests.get("https://aws.amazon.com/emr/").text
#soup = BeautifulSoup(html, "html.parser")

#print(soup.select("#aws-page-content-main > div:has(h2[id=How_it_works]) p"))