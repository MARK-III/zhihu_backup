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
cookie = '_zap=1dacec19-471e-4b4a-b2e4-7c1492fad30f; d_c0="APARiAnkdxGPToFkp7-VMzm5b_uSZjtoack=|1592883509"; _ga=GA1.2.970764465.1592883510; _xsrf=cae30116-fb4a-4d1f-a808-697f912b80cb; _gid=GA1.2.201703007.1593153659; capsion_ticket="2|1:0|10:1593154645|14:capsion_ticket|44:YzNmMGM0MmE5NWRmNDAzOGJkZjk4N2UyYmQwYzQxMzI=|d65cae80a0223188629b1d114343cf3626ed747ab936632e7c047840f2d6de38"; SESSIONID=tAQ3tYSt3wWBvMD4cEKVxGlnp8jshDMAXuqEv2LSS5P; JOID=V1kSAk2LuubhGkEBDI99_bVDq30f-_2x1W0cVH67ybelaw9BPt4mErsdQwENBtouywLV2GngKtqVeciZu7uFDvM=; osd=UlASBUyOs-bmG0QIDIh8-LxDrHwa8v221GgVVHm6zL6lbA5EN94hE74UQwYMA9MuzAPQ0WnnK9-cec-YvrKFCfI=; z_c0="2|1:0|10:1593154647|4:z_c0|92:Mi4xZUcwaUFBQUFBQUFBOEJHSUNlUjNFU1lBQUFCZ0FsVk5WLXJpWHdEY1docnkyVktaeWxOSlB0SXlJZ1NaWGloZkt3|c0d159d0907885bdac19b1d4935b147c2e4d7df3d1316029d9fa2c2c4d46b1eb"; tst=r; q_c1=2d2bd9133eaa44dfad478f4e84874ae6|1593156281000|1593156281000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1592883510,1593153657,1593156278,1593163691; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1593179495; KLBRSID=031b5396d5ab406499e2ac6fe1bb1a43|1593179517|1593179477'

#update_interval in days
update = 3
update_interval = 86400 * update

print 'zhihu archive start ...'

timestamp = int(time.time())

#sync following list

zhihu = Zhihu(archive_dir)
if timestamp - zhihu.timestamp() > update_interval:
    l = utils.get_follow_by_author(me, cookie)
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
    author = Author_C(archive_dir, a)
    print author.id
    if timestamp - author.timestamp() > update_interval:
        l = utils.get_collection_list_by_author(a, cookie)
        for collection in l:
            author.update(collection)
    else:
        print 'no need to update'

for a in author_list:
    author = Author_C(archive_dir, a)
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
