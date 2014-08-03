#!/usr/bin/python
# -*- coding: utf-8 -*-
import sql
import pre
import util
import cluster
import promote

top_id=['s_122', 'f_0062', 'c', 'k']
entainment_id=['f_0055', 's_112', 'k_5']
military_id=['f_0052', 's_122101', 'c_3']
society_id=['s_122102', 'f_0062-0003', 'c_4', 'k_3']
economy_id=['s_122104', 'f_0062-0005']
technogy_id=['s_122106', 'f_0062-0008']
inner_id=['s_122204', 'f_0062-0000', 'c_1', 'k_1']
internation_id=['s_122205', 'f_0062-0001', 'c_2', 'k_2']
sports_id=['s_16', 'f_0062-0006', 'k_4']
taiwan_id=['f_0062-0002', 'f_0052-0001']
property_id=['f_0062-0009']
category = [('top', top_id, 1), ('inner', inner_id, 3), ('military', military_id, 4), ('entainment', entainment_id, 5), ('internation', internation_id, 6),\
            ('sports', sports_id, 7), ('economy', economy_id, 8), ('society', society_id, 10)]
# category = [('top', top_id, 1)]
##category = [('sports', sports_id, 7)]
now, bef24, bef72 = util.getTime()
# now = '2014-07-30 21:47:20'
# bef24 = '2014-07-29 21:47:20'
# bef72 = '2014-07-27 21:47:20'

def getRes(news_category_id, category_id, category_name):
    news_corpus = sql.getNews(news_category_id, now)
    sounds_corpus = sql.getSound(category_id, bef72, now)
    news, sounds = pre.pre_all(news_corpus, sounds_corpus, now)
    
    index = -1
    for i, item in enumerate(sounds):
        if item[2] < bef24:
            index = i
            break

    if index == -1:
        print '12hour find error'
    print '72 hour sounds len:', len(sounds)
    print '24 hour sounds len:', index
    
    news_cluster = cluster.news_cluster(news, 0.2, now)
    sounds_cluster = cluster.sound_cluster(sounds[:index], 0.2, now)
    
    res = promote.start(news_cluster, sounds[:index], sounds, now, category_name, sounds_cluster)
    
    return res

def run():
    print 'start time: ', now
    util.mkDir('log/'+now)
    for item in category:
        category_name, category_id, news_category_id = item
        print category_name, category_id, news_category_id
        num, res = getRes(news_category_id, category_id, category_name)
        if num > 0:
            if sql.insPromoted(news_category_id, res, num):
                print 'sql ok'
            else:
                print 'sql error'
            print '------------------------------------\n'
        
if __name__ == '__main__':
    run()
