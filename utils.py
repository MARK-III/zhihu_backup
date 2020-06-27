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

def get_answers_by_author(archive_dir, author):
    print 'get all answers of: ' + author
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
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.find(attrs={'id': 'js-initialData'}) #get json tag
        text_json = str(tag).strip('<script id="js-initialData" type="text/json">').strip('</script>') #get json content
        dict_json = json.loads(text_json)
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
    with open(json_file, 'w') as json_f:
        json_f.write(json.dumps(answer_dict))
    json_f.close()




def send_api_request(url, headers, params):
    response =requests.get(url, headers=headers, params=params)
    html = response.text
    dict_json = json.loads(html)
    return dict_json

