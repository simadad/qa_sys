import requests
from bs4 import BeautifulSoup
import json
import threading
# from time import sleep

root_url = 'http://crossincode.com'
cookies = {
    'Cookie': 'UM_distinctid=15adb4ff6b028e-03562113aca7d7-556c3f70-100200-15adb4ff6b27e; pgv_pvi=4228580352; sessionid=9xhrhwi1uzfgph61e522yghjevqst8fk; pgv_si=s8882402304; csrftoken=1ouKBUKgAyDtVezDm7EAlWTgxqssFtmc'
}
error = []


def _get_answer(url):
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    desc = soup.find(class_='panel-body').prettify()
    # print(desc.prettify())
    print('DESC-len:\t', len(desc))
    answer = soup.find(class_='panel-footer').prettify()
    # print(answer.prettify())
    # answer = ''.join(answer.stripped_strings)
    print('ANSWER-len:\t', len(answer))
    # sleep(0.5)
    return desc, answer


def _save_item(title, desc, answer):
    url = 'http://127.0.0.1:8000/qa/save'
    data = {
        'title': title,
        'desc': desc,
        'answer': answer,
    }
    r = requests.post(url, data=data)
    reply = json.loads(r.text)
    print('SAVE-item:\t', reply)
    return reply.get('qid')


def _save_keyword(key, qid):
    url = 'http://127.0.0.1:8000/qa/k2qa'
    data = {
        'key': key,
        'qid': qid
    }
    r = requests.get(url, params=data)
    reply = json.loads(r.text)
    print('SAVE-key:\t', reply)


def thr_item(item):
    h4 = item.find('h4')
    title = h4.string
    item_url = h4.parent['href']
    tags = item.find_all('a', class_='tag')
    print('TITLE:\t', title)
    print('URL:\t', root_url + item_url)
    desc, answer = _get_answer(root_url + item_url)
    qid = _save_item(title, desc, answer)
    if qid:
        for tag in tags:
            print('TAG:\t', tag.string)
            _save_keyword(tag, qid)
    else:
        error.append(item_url)


def faq_spider():
    r = requests.get(root_url + '/faq/')
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all(attrs={'class': 'list-group-item'})
    tts = []
    numb = 0
    for item in items:
        numb += 1
        thr = threading.Thread(target=thr_item, args=(item,))
        tts.append(thr)
        if numb > 4:
            [t.start() for t in tts]
            [t.join() for t in tts]
            numb = 0
            tts = []

if __name__ == '__main__':
    faq_spider()
    for i in error:
        print(i)
