#coding:utf-8
import sys
import os
import json
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask
from flask import request
from flask import send_from_directory
from flask import url_for
from flask import redirect

app = Flask(__name__, static_url_path='')
archive_dir = 'archive'

@app.route('/')
def index():
    index_file = os.path.join(archive_dir, 'index.json')
    with open(index_file) as f:
        author_dict = json.loads(f.read())
    return author_dict

@app.route('/<people>/answer')
def people_answer_index(people):
    index_file = os.path.join(archive_dir, people, 'answer', 'index.json')
    with open(index_file) as f:
        answer_dict = json.loads(f.read())
    return answer_dict

@app.route('/<people>/answer/<answer_id>')
def people_answer_page(people, answer_id):
    answer_file = os.path.join(archive_dir, people, 'answer', answer_id + '.txt')
    with open(answer_file) as f:
        answer = f.read()
    return answer

@app.route('/<people>/collection')
def people_collection_index(people):
    index_file = os.path.join(archive_dir, people, 'collections', 'index.json')
    with open(index_file) as f:
        collection_dict = json.loads(f.read())
    return collection_dict

@app.route('/<people>/collection/<collection_id>')
def people_collection_answer_index(people, collection_id):
    index_file = os.path.join(archive_dir, people, 'collections', collection_id, 'index.json')
    with open(index_file) as f:
        answer_dict = json.loads(f.read())
    return answer_dict

@app.route('/<people>/collection/<collection_id>/<answer_id>')
def people_collection_answer_index(people, collection_id, answer_id):
    answer_file = os.path.join(archive_dir, people, 'collections', collection_id, answer_id + 'txt')
    with open(answer_file) as f:
        answer = f.read()
    return answer


if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.199.110', port=1080, threaded=True)