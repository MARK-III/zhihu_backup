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
import utils

    
def get_collections_by_author(author):
    print 'get all collections of: ' + author
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
        try:
            response =requests.get(url, headers=headers)
        except:
            print('anti spider, wait for 30 seconds and try again')
            time.sleep(30)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.find(attrs={'id': 'js-initialData'}) #get json tag
        text_json = str(tag).strip('<script id="js-initialData" type="text/json">').strip('</script>') #get json content
        dict_json = json.loads(text_json)
        drained = dict_json['initialState']['people']['favlistsByUser'][author]['isDrained']
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
        page = page + 1
        time.sleep(2)
    collections_dict['collections'] = collections

    with open(json_file, 'w') as json_f:
        json_f.write(json.dumps(collections_dict))
    json_f.close
    #for c in collections:
    #    get_answers_by_collection(str(c['id']), author)

def get_answers_by_collection(c_id, author):
    print 'get all answers of collection: ' + c_id
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
        response =requests.get(url, headers=headers, params=params)
        html = response.text
        dict_json = json.loads(html)
        drained = dict_json['paging']['is_end']   
        answer_dict['collector_id'] = author

        for a in dict_json['data']:
            d = {}
            d['id'] = a['content']['id']
            d['author'] = a['content']['author']['url_token']
            #d['question_id'] = a['content']['question']['id']
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
            #d['createdTime'] = a['content']['created_time']
            #d['updatedTime'] = a['content']['updated_time']
            fname = str(d['id']) + '.txt'
            f = os.path.join(answer_folder, fname)
            with open(f, 'w') as txt_file:
                txt_file.write(d['content'])
            txt_file.close()
            answers.append(d)
        offset = offset + 20
        time.sleep(2)
    print 'total answers: ' + str(len(answers))
    answer_dict['answers'] = answers
    with open(json_file, 'w') as json_f:
        json_f.write(json.dumps(answer_dict))
    json_f.close()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    #'referer': 'https://www.zhihu.com/people/mcbig/answers?page=1',
    'referer': 'https://www.zhihu.com',
    'cookie': '_zap=1dacec19-471e-4b4a-b2e4-7c1492fad30f; d_c0="APARiAnkdxGPToFkp7-VMzm5b_uSZjtoack=|1592883509"; _ga=GA1.2.970764465.1592883510; _xsrf=cae30116-fb4a-4d1f-a808-697f912b80cb; _gid=GA1.2.201703007.1593153659; capsion_ticket="2|1:0|10:1593154645|14:capsion_ticket|44:YzNmMGM0MmE5NWRmNDAzOGJkZjk4N2UyYmQwYzQxMzI=|d65cae80a0223188629b1d114343cf3626ed747ab936632e7c047840f2d6de38"; SESSIONID=tAQ3tYSt3wWBvMD4cEKVxGlnp8jshDMAXuqEv2LSS5P; JOID=V1kSAk2LuubhGkEBDI99_bVDq30f-_2x1W0cVH67ybelaw9BPt4mErsdQwENBtouywLV2GngKtqVeciZu7uFDvM=; osd=UlASBUyOs-bmG0QIDIh8-LxDrHwa8v221GgVVHm6zL6lbA5EN94hE74UQwYMA9MuzAPQ0WnnK9-cec-YvrKFCfI=; z_c0="2|1:0|10:1593154647|4:z_c0|92:Mi4xZUcwaUFBQUFBQUFBOEJHSUNlUjNFU1lBQUFCZ0FsVk5WLXJpWHdEY1docnkyVktaeWxOSlB0SXlJZ1NaWGloZkt3|c0d159d0907885bdac19b1d4935b147c2e4d7df3d1316029d9fa2c2c4d46b1eb"; tst=r; q_c1=2d2bd9133eaa44dfad478f4e84874ae6|1593156281000|1593156281000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1592883510,1593153657,1593156278,1593163691; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1593179495; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1593179517|1593179477'
}

cookie = '_zap=1dacec19-471e-4b4a-b2e4-7c1492fad30f; d_c0="APARiAnkdxGPToFkp7-VMzm5b_uSZjtoack=|1592883509"; _ga=GA1.2.970764465.1592883510; _xsrf=cae30116-fb4a-4d1f-a808-697f912b80cb; _gid=GA1.2.201703007.1593153659; capsion_ticket="2|1:0|10:1593154645|14:capsion_ticket|44:YzNmMGM0MmE5NWRmNDAzOGJkZjk4N2UyYmQwYzQxMzI=|d65cae80a0223188629b1d114343cf3626ed747ab936632e7c047840f2d6de38"; SESSIONID=tAQ3tYSt3wWBvMD4cEKVxGlnp8jshDMAXuqEv2LSS5P; JOID=V1kSAk2LuubhGkEBDI99_bVDq30f-_2x1W0cVH67ybelaw9BPt4mErsdQwENBtouywLV2GngKtqVeciZu7uFDvM=; osd=UlASBUyOs-bmG0QIDIh8-LxDrHwa8v221GgVVHm6zL6lbA5EN94hE74UQwYMA9MuzAPQ0WnnK9-cec-YvrKFCfI=; z_c0="2|1:0|10:1593154647|4:z_c0|92:Mi4xZUcwaUFBQUFBQUFBOEJHSUNlUjNFU1lBQUFCZ0FsVk5WLXJpWHdEY1docnkyVktaeWxOSlB0SXlJZ1NaWGloZkt3|c0d159d0907885bdac19b1d4935b147c2e4d7df3d1316029d9fa2c2c4d46b1eb"; tst=r; q_c1=2d2bd9133eaa44dfad478f4e84874ae6|1593156281000|1593156281000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1592883510,1593153657,1593156278,1593163691; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1593179495; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1593179517|1593179477'

print 'zhihu archive start ...'

archive_dir = 'archive'

#sync following list
json_file = os.path.join(archive_dir, 'index.json')
if os.path.exists(archive_dir) and os.path.exists(json_file):
    print 'following list exists'
    pass
else:
    if not os.path.exists(archive_dir):
        print 'new node, create archive folder'
        os.makedirs(archive_dir)
    print 'sync following list'
    utils.get_follow_by_author(archive_dir, 'xjq314', cookie)

#sync answer by author
author_folders = os.listdir(archive_dir)
for f in author_folders:
    if f != 'index.json':
        print 'dealing with author: ' + f
        answer_folder = os.path.join(archive_dir, f, 'answer')
        json_file = os.path.join(answer_folder, 'index.json')
        if os.path.exists(answer_folder) and os.path.exists(json_file):
            print 'answer list exists'
        else:
            if not os.path.exists(answer_folder):
                print 'new followee, create answer folder'
                os.makedirs(answer_folder)
            print 'sync answers of author: ' + f
            utils.get_answers_by_author(archive_dir, f, cookie)

#sync collection by author
author_folders = os.listdir(archive_dir)
for f in author_folders:
    if f != 'index.json':
        print 'dealing with author: ' + f
        collection_folder = os.path.join(archive_dir, f, 'collections')
        if os.path.exists(collection_folder):
            json_file = os.path.join(collection_folder, 'index.json')
            if os.path.exists(json_file):
                print 'collection list exists'
            else:
                print 'sync collection of author: ' + f
                get_collections_by_author(f)
        else:
            print 'new followee, create collection folder'
            os.makedirs(collection_folder)
            print 'sync collection of author: ' + f
            get_collections_by_author(f)