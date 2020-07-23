import os
import time
import sys
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import utils
from zhihu import *

me = 'xjq314'
archive_dir = 'archive'
cookie = '_zap=5fd22f92-8453-45b2-b8db-d6f3ae718f6a; d_c0="AADR_D8adBGPTpAp4CCVjA4Q9--O9081LMk=|1592629285"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1592630061,1592722829,1592730289,1593011286; _ga=GA1.2.186257978.1592629287; _xsrf=14YsIRPYeljzGOsTnokyWc2BcICFLs85; z_c0="2|1:0|10:1592630071|4:z_c0|92:Mi4xZUcwaUFBQUFBQUFBQU5IOFB4cDBFU1lBQUFCZ0FsVk5OLW5hWHdBZDJXTXlER3RrU2JvLVV1SzAtdGZES21xdFBB|2c27981f90899318a98ca8dd6ed20d7f05495d32115d93058f04d72ea65af277"; tst=r; q_c1=aff8d03f0efd4f459c3642aa4c8cca45|1593852517000|1593852517000; KLBRSID=fb3eda1aa35a9ed9f88f346a7a3ebe83|1595352814|1595352808; SESSIONID=x5GHL5yYlaXaN6GQxcuWNlnblRhXEyjAaiMWllFIKhM; JOID=U1wdBk743XGk7cmpS_yc4igWjSJTheQ77KX53B-QuSXIo_vrFh36a__swKhGH4SY3sAA6NOa7zUzyT5hZDjkOW4=; osd=UF4cAkz733Cg78qrSvie4SoXiSBQh-U_7qb73RuSuifJp_noFBz-afzuwaxEHIaZ2sID6tKe7TYxyDpjZzrlPWw='

#update_interval in days
update = 3
update_interval = 86400 * update

print 'zhihu archive start ...'

timestamp = int(time.time())

#sync following list

zhihu = User(archive_dir, me)
if timestamp - zhihu.timestamp > update_interval:
    l = utils.get_follow_by_author2(me, cookie)
    for a in l:
        zhihu.update(a)
else:
    print 'no need to update'

author_list = zhihu.followee_list()
for a in author_list:
    author = Author(archive_dir, a)
    print author.id
    if timestamp - author.timestamp() > update_interval:
        l = utils.get_answers_by_author(a, cookie)
        for answer in l:
            author.update(answer)
        author._save()
    else:
        print 'no need to update'

for a in author_list:
    author = Author_Collection(archive_dir, a)
    print author.id
    if timestamp - author.timestamp() > update_interval:
        l = utils.get_collection_list_by_author(a, cookie)
        for collection in l:
            author.update(collection)
    else:
        print 'no need to update'

for a in author_list:
    author = Author_Collection(archive_dir, a)
    print author.id
    collection_list = author.collection_list()
    for c in collection_list:
        collection = Collection(archive_dir, a, c)
        if timestamp - collection.timestamp() > update_interval:
            l = utils.get_answers_by_collection(c, cookie)
            for answer in l:
                collection.update(answer)
            if len(l) == 0:
                collection._save()
        else:
            print 'no need to update'

timestamp_end = int(time.time())
duration = timestamp_end - timestamp
print 'time spend: ' + str(duration) + 's'

#create a zip file
#generate pdf file

print 'end of program'
