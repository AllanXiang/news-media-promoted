# -*- coding: utf-8 -*-
import datetime
import time
import sys,os
#sys.path.append('/home/xzy/PythonFiles/FM/')

def StopWords():
    """
    load stopwords from file(conf/StopWords.txt)
    """
    stopwords = []
    fp_stopwords =open('conf/StopWords.txt', 'r')
    for line in fp_stopwords:
        stopwords.append(line.strip())
    fp_stopwords.close()
    return stopwords

def getNow():
    """
    return now
    format: %Y-%m-%d %H:%M:%S
    """
    now  = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return  now
    
def mkDir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print 'create folder', folder
    else:
        print 'exist'

def checktime(base, sound_time):
    '''
    check whether the sound happen in 12 hour 
    '''
    if len(sound_time) == 16:
        sound_time += ':00'
    t1 = time.strptime(base, '%Y-%m-%d %H:%M:%S')
    t2 = time.strptime(sound_time, '%Y-%m-%d %H:%M:%S')
    interval = (time.mktime(t1)-time.mktime(t2))/3600
    if interval <= 12.0:
        return True
    else:
        return False
    
def sub_time(time1, time2):
    t1 = time.strptime(time1, '%Y-%m-%d %H:%M:%S')
    t2 = time.strptime(time2, '%Y-%m-%d %H:%M:%S')
    interval = (time.mktime(t1)-time.mktime(t2))/3600
    return interval


def dt2str(news_time):
    return news_time.strftime('%Y-%m-%d %H:%M:%S')
