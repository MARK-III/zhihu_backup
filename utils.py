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
us_retry_wait = 15

def get_follow_by_author(author, cookie):
    result = []
    print 'get all follow of: ' + author
    headers = _header(cookie)
    drained = False
    base_url = 'https://www.zhihu.com/api/v4/members/'
    url = base_url + author + '/followees'
    offset = 0
    while not drained:
        print 'get ' + author + '\'s followee offset: ' + str(offset)
        params = {
            'offset': offset,
            'limit': 20,
            'include': 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
            }
        try:
            response =requests.get(url, headers=headers, params=params)
        except:
            print('network error, wait for ' + str(us_retry_wait) + ' seconds and try again')
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
    print 'get all answers: ' + author
    result = []
    headers = _header(cookie)
    drained = False
    base_url = 'https://zhihu.com/people/'
    url = base_url + author + '/answers'
    page = 1
    while not drained:
        print author + '\'s answer get page: ' + str(page)
        params = {
            'page': page
        }
        try:
            response =requests.get(url, headers=headers, params=params, timeout=15)
        except:
            print('network error, wait for ' + str(us_retry_wait) + ' seconds and try again')
            time.sleep(us_retry_wait)
            continue
        dict_json = _html_to_json(response.text)
        drained = dict_json['initialState']['people']['answersByUser'][author]['isDrained']              
        answer_list = dict_json['initialState']['entities']['answers']
        for id in answer_list.keys():
            a = {
                'id' : id,
                'question_id' : answer_list[id]['question']['id'],
                'title' : answer_list[id]['question']['title'],
                'createdTime' : answer_list[id]['createdTime'],
                'updatedTime' : answer_list[id]['updatedTime'],
                'contents' : answer_list[id]['content']
            }
            result.append(a)
        page = page + 1
        time.sleep(us_request_wait)
    print 'total answers: ' + str(len(result))
    return result

def get_collection_list_by_author(author, cookie):
    print 'get all collections of: ' + author
    headers = _header(cookie)
    result = []
    drained = False
    base_url = 'https://zhihu.com/people/'
    url = base_url + author + '/collections'
    page = 1
    while not drained:
        print 'get ' + author + '\'s collection page: ' + str(page)
        params = {
            'page': page
        }
        try:
            response =requests.get(url, headers=headers, params=params)
        except:
            print('network error, wait for ' + str(us_retry_wait) + ' seconds and try again')
            time.sleep(us_retry_wait)
            continue
        dict_json = _html_to_json(response.text)
        drained = dict_json['initialState']['people']['favlistsByUser'][author]['isDrained']
        total = dict_json['initialState']['people']['favlistsByUser'][author]['totals']
        flavor_list = dict_json['initialState']['entities']['favlists']
        for id in flavor_list:
            d = {
                'id' : id,
                'answerCount' : flavor_list[id]['answerCount'],
                'title' : flavor_list[id]['title'],
                'createdTime' : flavor_list[id]['createdTime'],
                'updatedTime' : flavor_list[id]['updatedTime']
            }
            result.append(d)
        if len(result) >= total:
            drained = True
        page = page + 1
        time.sleep(us_request_wait)
    return result

def get_answers_by_collection(c_id, cookie):
    print 'get all answers of collection: ' + c_id
    headers = _header(cookie)
    result = []
    drained = False
    base_url = 'https://www.zhihu.com/api/v4/favlists/'
    url = base_url + c_id + '/items'
    offset = 0
    while not drained:
        print 'get ' + str(c_id) + ' answers from: ' + str(offset)
        params = {
            'offset': offset,
            'limit': 20,
            'include': 'data[*].created,content.comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,description,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,is_recognized;data[*].author.badge[?(type=best_answerer)].topics'
        }
        try:
            response =requests.get(url, headers=headers, params=params)
        except:
            print('network error, wait for ' + str(us_retry_wait) + ' seconds and try again')
            time.sleep(us_retry_wait)
            continue
        dict_json = json.loads(response.text)
        drained = dict_json['paging']['is_end']   
        for a in dict_json['data']:
            d = {
                'id' : a['content']['id'],
                'author' : a['content']['author']['url_token'],
                'content' : '',
                'title' : '',
                'updatedTime': 0,
                'type': a['content']['type'],
                'question_id': '',
                'type': a['content']['type']
            }
            if a['content']['type'] == 'answer':
                d['title'] = a['content']['question']['title']
                d['updatedTime'] = a['content']['updated_time']
                d['content'] = a['content']['content']
                d['question_id'] = a['content']['question']['id']
                result.append(d)
            if a['content']['type'] == 'article':
                d['title'] = a['content']['title']
                d['updatedTime'] = a['content']['updated']
                d['content'] = a['content']['content']
                result.append(d)
        offset = offset + 20
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
    
