#!/usr/bin/python3
import requests
import json
from time import sleep


def setlabel(qid, language, value, token):
    sleep(5)
    response = requests.post(WIKISITE, {
        'action': 'wbsetlabel',
        'id': qid,
        'language': language,
        'value': value,
        'token': token
    })
    return response


def setdescription(qid, language, value, token):
    sleep(5)
    response = requests.post(WIKISITE, {
        'action': 'wbsetdescription',
        'id': qid,
        'language': language,
        'value': value,
        'token': token
    })
    return response


WIKISITE = 'https://www.wikidata.org/w/api.php'
SITES = 'ruwiki'

tokenget = requests.get(WIKISITE, {
    'action': 'query',
    'meta': 'tokens',
    'format': 'json'})

TOKEN = tokenget.json()['query']['tokens']['csrftoken']
# TOKEN = '+\\'

with open('a.json', 'r') as f:
    airman = json.load(f)

for name in airman:
    print(airman[name]['qid'], '-', name)
    ojson = requests.get(WIKISITE, {
        'action': 'wbgetentities',
        'titles': name,
        'sites': SITES,
        'format': 'json'
    }).json()

    if ojson['success'] != 1:
        print('Not success')

    qidthis = list(ojson['entities'])[0]
    if len(list(ojson['entities'])) > 1:
        print('Non one element: ')
        for elem in list(ojson['entities']):
            print(ojson['entities'][list(ojson['entities'])[0]]
                  ['labels']['ru']['value'])
    try:
        if (airman[name]['qid'] != qidthis):
            print('wrong Q id')
            exit(-1)
    except Exception as e:
        pass
    try:
        print('nameen', airman[name]['nameen'] == ojson['entities'][qidthis]['labels']['en']['value'])
        if (airman[name]['nameen'] != ojson['entities'][qidthis]['labels']['en']['value']):
            setlabel(qidthis, 'en', airman[name]['nameen'], TOKEN)
    except Exception as e:
        setlabel(qidthis, 'en', airman[name]['nameen'], TOKEN)
    try:
        print('des', airman[name]['description'] == ojson['entities'][qidthis]['descriptions']['ru']['value'])
        if (airman[name]['description'] != ojson['entities'][qidthis]['descriptions']['ru']['value']):
            setdescription(qidthis, 'ru', airman[name]['description'], TOKEN)
    except Exception as e:
        setdescription(qidthis, 'ru', airman[name]['description'], TOKEN)
    try:
        print('desen', airman[name]['descriptionen'] == ojson['entities'][qidthis]['descriptions']['en']['value'])
        if (airman[name]['descriptionen'] != ojson['entities'][qidthis]['descriptions']['en']['value']):
            setdescription(qidthis, 'en', airman[name]['descriptionen'], TOKEN)
    except Exception as e:
        setdescription(qidthis, 'en', airman[name]['descriptionen'], TOKEN)
    # exit(-1)
    sleep(10)
