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
from flask import render_template
from flask import redirect
from zhihu import *

app = Flask(__name__, static_url_path='')
archive_dir = 'archive'

@app.route('/')
def index():
    title = 'zhihu_archive'
    zhihu = User(archive_dir)  
    followee_list = zhihu.followee_list_for_frontend()
    return render_template('index.html', title=title, list=followee_list)

@app.route('/people/<people>/answer')
def people_answer_index(people):
    author = Author(archive_dir, people)
    answer_list = author.answer_list_for_frontend()
    return render_template('answer_list.html', title=people, list=answer_list)

@app.route('/people/<people>/answer/<answer_id>')
def people_answer_page(people, answer_id):

    answer_file = os.path.join(archive_dir, people, 'answer', answer_id + '.txt')
    with open(answer_file) as f:
        answer = f.read()
    return answer

@app.route('/people/<people>/collection')
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
def people_collection_answer_page(people, collection_id, answer_id):
    answer_file = os.path.join(archive_dir, people, 'collections', collection_id, answer_id + 'txt')
    with open(answer_file) as f:
        answer = f.read()
    return answer


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=1080, threaded=True)