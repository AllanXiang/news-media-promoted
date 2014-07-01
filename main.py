# -*- coding: utf-8 -*-

import sql
import pre
import util
import cluster
import promote

top_id=['s_122', 'f_0062', 'c']
entainment_id=['f_0055', 's_112']
military_id=['f_0052', 's_122101', 'c_3']
society_id=['s_122102', 'f_0062-0003', 'c_4']
economy_id=['s_122104', 'f_0062-0005']
technogy_id=['s_122106', 'f_0062-0008']
inner_id=['s_122204', 'f_0062-0000', 'c_1']
internation_id=['s_122205', 'f_0062-0001', 'c_2']
sports_id=['s_16', 'f_0062-0006']
taiwan_id=['f_0062-0002', 'f_0052-0001']
property_id=['f_0062-0009']
##category = [('top', top_id, 1), ('inner', inner_id, 3), ('military', military_id, 4), ('entainment', entainment_id, 5), ('internation', internation_id, 6),\
##            ('sports', sports_id, 7), ('economy', economy_id, 8), ('society', society_id, 10)]
category = [('top', top_id, 1)]
##category = [('sports', sports_id, 7)]
now = util.getNow()

def getRes(news_id, category_id, category_name):
    news_text, news_downtime = sql.getNews(news_id, now)
    
    sound_id = []
    sound_downtime = []
    
    train_id = []
    train_text = []
    train_downtime = []
    
    for id in category_id:
        tmp_sound_id, tmp_sound_downtime = sql.getSound(id, now, isTrain=False)
        sound_id.extend(tmp_sound_id)
        sound_downtime.extend(tmp_sound_downtime)
        print id, len(tmp_sound_id)
        
        tmp_train_id, tmp_train_text, tmp_train_downtime = sql.getSound(id, isTrain=True)
        train_downtime.extend(tmp_train_downtime)
        train_id.extend(tmp_train_id)
        train_text.extend(tmp_train_text)

    print 'sounds tot:', len(sound_id)
##    最近24小时sound排序
    tmp = zip(sound_id, sound_downtime)
    tmp.sort(key=lambda item: item[1], reverse=True)
    sound_id, sound_downtime = zip(*tmp)
    
    news_seg, news_scores, train_seg = pre.pre_all(news_text, news_downtime, train_text, now)
    selected = cluster.cos_tfidf(news_seg, news_scores, 0.3)
    res = promote.start(selected, sound_id, sound_downtime, train_id, train_seg, train_downtime, now, category_name)
    
    return res

def run():
    print 'start time: ', now
    util.mkDir('log/'+now)
    for item in category:
        category_name, category_id, news_id = item
        print category_name, category_id, news_id
        num, res = getRes(news_id, category_id, category_name)
##        getRes(news_id, category_id, category_name)

##        if sql.insPromoted(news_id, res, num):
##            print 'sql ok'
##        else:
##            print 'sql error'
##        print '------------------------------------\n'
        
if __name__ == '__main__':
    run()
