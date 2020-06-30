import sys
import os
import json
import time
reload(sys)
sys.setdefaultencoding("utf-8")


class Zhihu():

    def __init__(self, archive_dir):
        self.archive_dir = archive_dir
        self.json_file = os.path.join(archive_dir, 'index.json')
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.meta = json.loads(f.read())
                f.close()
        else:
            self.meta = {}
    
    def list_followees(self):
        for i in self.meta['followee']:
            print i['name']
    
    def merge_answers(self):
        for i in self.meta['followees'].keys():
            index_file = os.path.join(self.archive_dir, i, 'answer', 'index.json')
            self.meta['followees'][i]['answers'] = dict()
            try:
                with open(index_file) as f:
                    answer_dict = json.loads(f.read())
                    f.close()
            except:
                del self.meta['followees'][i]
                continue
            answer_list = answer_dict['answers']
            for answer in answer_list:
                del answer['content']
                self.meta['followees'][i]['answers'][answer['id']] = answer

    def save(self):
        timestamp = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        newname = self.json_file + '.' + timestamp
        os.rename(self.json_file, newname)
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.meta))
            f.close()

class Author():

    def __init__(self, archive_dir, author_id):
        self.archive_dir = archive_dir
        self.json_file = os.path.join(archive_dir, author_id, 'answer', 'index.json')
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.meta = json.loads(f.read())
                f.close()
        else:
            self.meta = {}
        
    def save(self):
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.meta))
            f.close()
    
    def answer_ls(self):
        for key in self.meta['answers'].keys():
            print key

class Author_c():

    def __init__(self, archive_dir, author_id):
        self.archive_dir = archive_dir
        self.json_file = os.path.join(archive_dir, author_id, 'collections', 'index.json')
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.meta = json.loads(f.read())
                f.close()
        else:
            self.meta = {}
    
    def collection_ls(self):
        l = []
        for c in self.meta['collections']:
            l.append(c['id'])
            print c['id']
        return l
        
    def save(self):
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.meta))
            f.close()


class Collection():

    def __init__(self, archive_dir, author_id, c_id):
        self.archive_dir = archive_dir
        self.json_file = os.path.join(archive_dir, author_id, 'collections', c_id, 'index.json')
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.meta = json.loads(f.read())
                f.close()
        else:
            self.meta = {}
        
    def save(self):
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.meta))
            f.close()
    
    def answer_ls(self):
        for key in self.meta['answers'].keys():
            print key