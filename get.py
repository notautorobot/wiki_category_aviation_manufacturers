#!/usr/bin/python3
import requests
import json

WIKISITE = 'https://www.wikidata.org/w/api.php'
SITES = 'ruwiki'

with open('a.json', 'r') as f:
    airman = json.load(f)

for name in airman:
    resp = requests.get(WIKISITE, {
        'action': 'wbgetentities',
        'titles': name,
        'sites': SITES,
        'format': 'json'
    }).json()
    # print(resp)
    ojson = resp
    # with open('2') as f:
    #     ojson = json.load(f)
    # print(ojson)

    if ojson['success'] != 1:
        print('Not success')

    if len(list(ojson['entities'])) > 1:
        print('Non one element: ')
        for elem in list(ojson['entities']):
            print(ojson['entities'][list(ojson['entities'])[0]]
                  ['labels']['ru']['value'])
    try:
        airman[name]['qid'] = list(ojson['entities'])[0]
    except Exception as e:
        pass
    try:
        airman[name]['nameen'] = ojson['entities'][list(ojson['entities'])[0]]['labels']['en']['value']
    except Exception as e:
        try:
            airman[name]['nameen'] = ojson['entities'][list(ojson['entities'])[0]]['sitewiki']['enwiki']['title']
        except Exception as e:
            pass
    try:
        airman[name]['description'] = ojson['entities'][list(ojson['entities'])[0]]['descriptions']['ru']['value']
    except Exception as e:
        pass
    try:
        airman[name]['descriptionen'] = ojson['entities'][list(ojson['entities'])[0]]['descriptions']['en']['value']
    except Exception as e:
        pass

with open('a.json', 'w') as ff:
    json.dump(airman, ff)

