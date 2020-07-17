import sys
import os
import json
import time
reload(sys)
sys.setdefaultencoding("utf-8")


class Zhihu():

    def __init__(self, archive_dir):
        self.archive_dir = archive_dir
        if not os.path.exists(archive_dir):
            os.mkdir(self.archive_dir)
        self.json_file = os.path.join(archive_dir, 'index.json')
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.meta = json.loads(f.read())
        else:
            self.meta = {}
            self.meta['timestamp'] = int(time.time())
            self.meta['author_id'] = 'xjq314'
            self.meta['followees'] = dict()
        self.timestamp = self.meta['timestamp']

    def followee_list(self):
        l = []
        for key in self.meta['followees'].keys():
            l.append(key)
        return(l)
    
    def followee_list_for_frontend(self):
        l = []
        for i in self.meta['followees'].keys():
            d = self.meta['followees'][i]
            d['answer_url'] = '/people/' + i + '/answer'
            d['collection_url'] = '/people/' + i + '/collection'
            l.append(d)
        return(l)
    
    def update(self, a):
        if a['gender'] >= 0:
            self.meta['followees'][a['id']] = a
        author_dir = os.path.join(self.archive_dir, a['id'])
        if not os.path.exists(author_dir):
            os.mkdir(author_dir)
        self._save()

    def _save(self):
        self.meta['timestamp'] = int(time.time())
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.meta))
        
    def checksum(self):
        pass

class Author():

    def __init__(self, archive_dir, author_id):
        self.id = author_id
        self.archive_dir = archive_dir
        self.json_file = os.path.join(archive_dir, author_id, 'answer', 'index.json')
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.meta = json.loads(f.read())
        else:
            answer_dir = os.path.join(archive_dir, author_id, 'answer')
            if not os.path.exists(answer_dir):
                os.mkdir(answer_dir)
            self.meta = {}
            self.meta['answers'] = {}
            self.meta['author_id'] = self.id
            self.meta['timestamp'] = int(time.time())
    
    def timestamp(self):
        return self.meta['timestamp']
        
    def _save(self):
        timestamp = int(time.time())
        self.meta['timestamp'] = timestamp
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.meta))
    
    def answer_list_for_frontend(self):
        l = []
        for i in self.meta['answers'].keys():
            d = self.meta['answers'][i]
            d['url'] = '/people/' + self.id + '/answer/' + str(i)
            l.append(d)
        return(l)
    
    def update(self, a):
        if not a['id'] in self.meta['answers'].keys():
            print 'new answer:'
            print a['title']
            print a['contents']
            self._update_answer_file(a['id'], a['contents'])
            del a['contents']
            self.meta['answers'][a['id']] = a
            self._save()
            return None
        if a['updatedTime'] > self.meta['answers'][a['id']]['updatedTime']:
            print 'update answer:'
            print a['title']
            print a['contents']
            self._update_answer_file(a['id'], a['contents'])
            del a['contents']
            self.meta['answers'][a['id']] = a
            self._save()
            return None
        return None
    
    def _update_answer_file(self, answer_id, text):
        answer_file = os.path.join(self.archive_dir, self.id, 'answer', answer_id + '.txt')
        if os.path.exists(answer_file):
            timestamp = int(time.time())
            archive_file = os.path.join(self.archive_dir, self.id, 'answer', answer_id + '.txt.' + str(timestamp))
            os.rename(answer_file, archive_file)
        with open(answer_file, 'w') as f:
            f.write(text)

    def checksum(self):
        print self.id
        for i in self.meta['answers'].keys():
            answer_file = os.path.join(self.archive_dir, self.id, 'answer', i + '.txt')
            if not os.path.exists(answer_file):
                pass
                #print 'file miss: ' + i
        answer_dir = os.path.join(self.archive_dir, self.id, 'answer')
        for f in os.listdir(answer_dir):
            ff =  f.strip('.txt')
            if not ff in self.meta['answers'].keys() and ff != 'index.json':
                print 'meta miss: ' + ff

class Author_C():

    def __init__(self, archive_dir, author_id):
        self.id = author_id
        self.archive_dir = archive_dir
        self.json_file = os.path.join(archive_dir, author_id, 'collections', 'index.json')
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.meta = json.loads(f.read())
        else:
            collections_dir = os.path.join(archive_dir, author_id, 'collections')
            if not os.path.exists(collections_dir):
                os.mkdir(collections_dir)
            self.meta = {}
            self.meta['author_id'] = self.id
            self.meta['collections'] = {}
            self.meta['timestamp'] = int(time.time())
    
    def collection_list(self):
        l = []
        for c in self.meta['collections'].keys():
            l.append(c)
        return l
    
    def update(self, a):
        self.meta['collections'][a['id']] = a
        collection_dir = os.path.join(self.archive_dir, self.id, 'collections', a['id'])
        if not os.path.exists(collection_dir):
            os.mkdir(collection_dir)
        self._save()
    
    def timestamp(self):
        return self.meta['timestamp']
        
    def _save(self):
        timestamp = int(time.time())
        self.meta['timestamp'] = timestamp
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.meta))

    def checksum(self):
        for i in self.meta['collections'].keys():
            collection_dir = os.path.join(self.archive_dir, self.id, 'collections', i)
            if not os.path.exists(collection_dir):
                print '====folder miss=====: ' + i
        collection_folder = os.path.join(self.archive_dir, self.id, 'collections')
        for f in os.listdir(collection_folder):
            if not f in self.meta['collections'].keys() and f != 'index.json':
                print '=====meta miss======: ' + f

class Collection():

    def __init__(self, archive_dir, author_id, c_id):
        self.id = c_id
        self.author_id = author_id
        self.archive_dir = archive_dir
        self.json_file = os.path.join(archive_dir, author_id, 'collections', c_id, 'index.json')
        
        
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.meta = json.loads(f.read())
        else:
            collection_dir = os.path.join(archive_dir, author_id, 'collections', c_id)
            if not os.path.exists(collection_dir):
                os.mkdir(collection_dir)
            self.meta = {}
            self.meta['author_id'] = self.id
            self.meta['answers'] = {}
            self.meta['timestamp'] = 0
            self.meta['url'] = ''
    
    def update(self, a):
        if not a['id'] in self.meta['answers'].keys():
            print 'new answer:'
            print a['title']
            self._update_answer_file(a['id'], a['content'])
            del a['content']
            self.meta['answers'][a['id']] = a
            print a
            self._save()
            return None
        if a['updatedTime'] > self.meta['answers'][a['id']]['updatedTime']:
            print 'update answer:'
            print a['title']
            self._update_answer_file(a['id'], a['contents'])
            del a['contents']
            self.meta['answers'][a['id']] = a
            self._save()
            return None
        return None
    
    def _update_answer_file(self, answer_id, text):
        answer_file = os.path.join(self.archive_dir, self.author_id, 'collections', self.id, str(answer_id) + '.txt')
        if os.path.exists(answer_file):
            timestamp = int(time.time())
            archive_file = os.path.join(answer_file + '.' + str(timestamp))
            os.rename(answer_file, archive_file)
        with open(answer_file, 'w') as f:
            f.write(text)

    def _save(self):
        timestamp = int(time.time())
        self.meta['timestamp'] = timestamp
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.meta))
    
    def timestamp(self):
        return self.meta['timestamp']
    
    def answer_ls(self):
        for key in self.meta['answers'].keys():
            print key

    def checksum(self):
        for i in self.meta['answers'].keys():
            answer_file = os.path.join(self.archive_dir, self.author_id, 'collections', self.id, i + '.txt')
            if not os.path.exists(answer_file):
                print '===file miss===: ' + i
        answer_dir = os.path.join(self.archive_dir, self.author_id, 'collections', self.id)
        for f in os.listdir(answer_dir):
            ff =  f.strip('.txt')
            if not ff in self.meta['answers'].keys() and ff != 'index.json':
                print '===meta miss===: '
                print self.author_id
                print self.id
                print ff
                self._rebuild_meta(ff)
                
