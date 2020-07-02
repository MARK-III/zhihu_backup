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
from zhihu import *

us_request_wait = 0
us_retry_wait = 20

def get_collections_by_author(archive_dir, author, cookie):
    print 'get all collections of: ' + author
    headers = _header(cookie)
    collections_dict = {}
    collections = []
    collections_folder = os.path.join(archive_dir, author, 'collections')
    if not os.path.exists(collections_folder):
        os.makedirs(collections_folder)
    json_file = os.path.join(collections_folder, 'index.json')
    drained = False
    base_url = 'https://zhihu.com/people/'
    url = base_url + author + '/collections'
    page = 1
    while not drained:
        print 'get page: ' + str(page)
        params = {
            'page': page
        }
        try:
            response =requests.get(url, headers=headers, params=params)
        except:
            print('anti spider, wait for ' + str(us_retry_wait) + ' seconds and try again')
            time.sleep(us_retry_wait)
            continue
        html = response.text
        #print html
        dict_json = _html_to_json(html)
        drained = dict_json['initialState']['people']['favlistsByUser'][author]['isDrained']
        total = dict_json['initialState']['people']['favlistsByUser'][author]['totals']
        collections_dict['author_id'] = author 
        flavor_list = dict_json['initialState']['entities']['favlists']
        for id in flavor_list:
            d = {}
            d['id'] = id
            d['answerCount'] = flavor_list[id]['answerCount']
            d['title'] = flavor_list[id]['title']
            d['createdTime'] = flavor_list[id]['createdTime']
            d['updatedTime'] = flavor_list[id]['updatedTime']
            collection_folder = os.path.join(collections_folder, id)
            if not os.path.exists(collection_folder):
                os.makedirs(collection_folder)
            collections.append(d)
        if len(collections) >= total:
            drained = True
        page = page + 1
        time.sleep(us_request_wait)
    collections_dict['collections'] = collections
    _json_to_file(collections_dict, json_file)

def get_collections_by_author2(archive_dir, author, cookie):
    print 'get all collections of: ' + author
    headers = _header(cookie)
    collections_dict = {}
    collections = []
    collections_folder = os.path.join(archive_dir, author, 'collections')
    if not os.path.exists(collections_folder):
        os.makedirs(collections_folder)
    json_file = os.path.join(collections_folder, 'index.json')
    drained = False
    base_url = 'https://www.zhihu.com/api/v4/members/'
    url = base_url + author + '/favlists'
    offset = 0
    while not drained:
        print 'get collection from: ' + str(offset)
        params = {
            'offset': offset,
            'limit': 20,
            'include': 'data[*].updated_time,answer_count,follower_count,creator,description,is_following,comment_count,created_time'
        }
        try:
            response =requests.get(url, headers=headers, params=params)
        except:
            print('anti spider, wait for ' + str(us_retry_wait) + ' seconds and try again')
            time.sleep(us_retry_wait)
            continue
        html = response.text
        print html
        dict_json = json.loads(html)
        drained = dict_json['paging']['is_end']  
        if drained:
            print 'drained'
        else:
            print 'not drained'
        collections_dict['author_id'] = author 
        flavor_list = dict_json['data']
        for id in flavor_list:
            d = {}
            d['url'] = id['url']
            d['id'] = id['id']
            d['answerCount'] = id['answerCount']
            d['title'] = id['title']
            d['createdTime'] = id['createdTime']
            d['updatedTime'] = id['updatedTime']
            collection_folder = os.path.join(collections_folder, d['id'])
            if not os.path.exists(collection_folder):
                os.makedirs(collection_folder)
            collections.append(d)
        page = page + 1
        time.sleep(us_request_wait)
    collections_dict['collections'] = collections
    _json_to_file(collections_dict, json_file)

def get_answers_by_collection(archive_dir, c_id, author, cookie):
    print 'get all answers of collection: ' + c_id
    headers = _header(cookie)
    answer_dict = {}
    answers = []
    answer_folder = os.path.join(archive_dir, author, 'collections', c_id)
    if not os.path.exists(answer_folder):
        os.makedirs(answer_folder)
    json_file = os.path.join(answer_folder, 'index.json')
    drained = False
    base_url = 'https://www.zhihu.com/api/v4/favlists/'
    url = base_url + c_id + '/items'
    offset = 0
    while not drained:
        print 'get answers from: ' + str(offset)
        params = {
            'offset': offset,
            'limit': 20,
            'include': 'data[*].created,content.comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,description,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,is_recognized;data[*].author.badge[?(type=best_answerer)].topics'
        }
        try:
            response =requests.get(url, headers=headers, params=params)
        except:
            print('anti spider, wait for ' + str(us_retry_wait) + ' seconds and try again')
            time.sleep(us_retry_wait)
            continue
        html = response.text
        dict_json = json.loads(html)
        drained = dict_json['paging']['is_end']   
        answer_dict['collector_id'] = author
        for a in dict_json['data']:
            d = {}
            d['id'] = a['content']['id']
            d['author'] = a['content']['author']['url_token']
            try:
                if 'question' in a['content'].keys():
                    d['title'] = a['content']['question']['title']
                else:
                    d['title'] = a['content']['title']
                if 'content' in a['content'].keys():
                    d['content'] = a['content']['content']
                else:
                    d['content'] = a['content']['url']   #corner case when content is video
            except:
                print 'failed'
                continue
            fname = str(d['id']) + '.txt'
            f = os.path.join(answer_folder, fname)
            with open(f, 'w') as txt_file:
                txt_file.write(d['content'])
            answers.append(d)
        offset = offset + 20
        time.sleep(us_request_wait)
    print 'total answers: ' + str(len(answers))
    answer_dict['answers'] = answers
    _json_to_file(answer_dict, json_file)

def get_follow_by_author(author, cookie):
    result = []
    print 'get all follow of: ' + author
    headers = _header(cookie)
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
            print('anti spider, wait for ' + str(us_retry_wait) + ' seconds and try again')
            time.sleep(us_retry_wait)
            continue
        dict_json = json.loads(response.text)
        drained = dict_json['paging']['is_end']   
        for f in dict_json['data']:
            a = {
                'uuid': f['id'],
                'name': f['name'],
                'id': f['url_token'],
                'gender': f['gender']
            }
            result.append(a)
        offset = offset + 20
        time.sleep(us_request_wait)
    print 'total followees: ' + str(len(result))
    return result

def get_answers_by_author(author, cookie):
    print 'get all answers of: ' + author
    result = []
    headers = _header(cookie)
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
            response =requests.get(url, headers=headers, params=params, timeout=15)
        except:
            print('anti spider, wait for ' + str(us_retry_wait) + ' seconds and try again')
            time.sleep(us_retry_wait)
            continue
        dict_json = _html_to_json(response.text)
        drained = dict_json['initialState']['people']['answersByUser'][author]['isDrained']              
        answer_list = dict_json['initialState']['entities']['answers']
        for id in answer_list.keys():
            a = {}
            a['id'] = id
            a['question_id'] = answer_list[id]['question']['id']
            a['title'] = answer_list[id]['question']['title']
            a['createdTime'] = answer_list[id]['createdTime']
            a['updatedTime'] = answer_list[id]['updatedTime']
            a['contents'] = answer_list[id]['content']
            result.append(a)
        page = page + 1
        time.sleep(us_request_wait)
    print 'total answers: ' + str(len(result))
    return result
    
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

def _content_update(text, txt_file):
    
    if not os.path.exits(txt_file):
        with open(txt_file, 'w') as f:
            f.write(text)
    else:
        with open(txt_file, 'r') as f:
            old_text = f.read()
        if len(old_text) != len(text):
            timestamp = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            newname = txt_file + '.' + timestamp
            os.rename(txt_file, newname)
            with open(txt_file, 'w') as f:
                f.write(text)




