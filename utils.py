import os
import time
from bs4 import BeautifulSoup
import requests
import json
import sys
import random
import pprint
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_answers_by_author(archive_dir, author, cookie):
    print 'get all answers of: ' + author
    headers = _header(cookie)
    answer_dict = {}
    answers = []
    answer_folder = os.path.join(archive_dir, author, 'answer')
    if not os.path.exists(answer_folder):
        os.makedirs(answer_folder)
    json_file = os.path.join(answer_folder, 'index.json')
    drained = False
    base_url = 'https://zhihu.com/people/'
    url = base_url + author + '/answers'
    page = 1
    while not drained:
        print 'get page: ' + str(page)
        params = {
            'page': page
        }
        try:
            response =requests.get(url, headers=headers, params=params)
        except:
            print('anti spider, wait for 30 seconds and try again')
            time.sleep(30)
            continue
        html = response.text
        dict_json = _html_to_json(html)
        drained = dict_json['initialState']['people']['answersByUser'][author]['isDrained']        
        answer_dict['author_id'] = author        
        answer_list = dict_json['initialState']['entities']['answers']
        for id in answer_list:
            d = {}
            d['id'] = id
            d['question_id'] = answer_list[id]['question']['id']
            d['title'] = answer_list[id]['question']['title']
            d['content'] = answer_list[id]['content']
            d['createdTime'] = answer_list[id]['createdTime']
            d['updatedTime'] = answer_list[id]['updatedTime']
            fname = id + '.txt'
            f = os.path.join(answer_folder, fname)
            with open(f, 'w') as txt_file:
                txt_file.write(d['content'])
            txt_file.close()
            answers.append(d)
        page = page + 1
        time.sleep(2)
    print 'total answers: ' + str(len(answers))
    answer_dict['answers'] = answers
    _json_to_file(answer_dict, json_file)

def get_follow_by_author(archive_dir, author, cookie):
    print 'get all follow of: ' + author
    headers = _header(cookie)
    follow_dict = {}
    followees = []
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    json_file = os.path.join(archive_dir, 'index.json')
    drained = False
    base_url = 'https://www.zhihu.com/api/v4/members/'
    url = base_url + author + '/followees'
    offset = 0
    while not drained:
        print 'get followee from: ' + str(offset)
        params = {
            'offset': offset,
            'limit': 20,
            'include': 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
            }
        try:
            response =requests.get(url, headers=headers, params=params)
        except:
            print('anti spider, wait for 30 seconds and try again')
            time.sleep(30)
            continue
        html = response.text
        dict_json = json.loads(html)
        drained = dict_json['paging']['is_end']   
        follow_dict['follower_id'] = author
        for f in dict_json['data']:
            p = {}
            p['uuid'] = f['id']
            p['name'] = f['name']
            p['id'] = f['url_token']
            pfolder = os.path.join(archive_dir , p['id'])
            if not os.path.exists(pfolder):
                os.makedirs(pfolder)
            followees.append(p)
        offset = offset + 20
        time.sleep(2)
    print 'total followees: ' + str(len(followees))
    follow_dict['followee'] = followees
    _json_to_file(follow_dict, json_file)


def _html_to_json(html):
    #extract json from html working from 2020.06.28
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find(attrs={'id': 'js-initialData'}) #get json tag
    text_json = str(tag).strip('<script id="js-initialData" type="text/json">').strip('</script>') #get json content
    j = json.loads(text_json)
    return j

def _header(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'referer': 'https://www.zhihu.com',
        'cookie': cookie
        }
    return headers

def _json_to_file(j, f):
    with open(f, 'w')as json_f:
        json_f.write(json.dumps(j))
    json_f.close()


def send_api_request(url, headers, params):
    response =requests.get(url, headers=headers, params=params)
    html = response.text
    dict_json = json.loads(html)
    return dict_json


