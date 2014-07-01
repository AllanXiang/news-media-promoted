# -*- coding: utf-8 -*-
import MySQLdb
import util
'''
    查询24小时内新闻
'''
def getNews(news_id, downtime):
    conn = MySQLdb.connect(host='10.141.201.62', user='root', passwd='medlab', db='media', charset='utf8')
    cur = conn.cursor()
    sql = "select contents,downloadtime from news where downloadtime >= '%s'-interval 24 hour and categoryid = '%d' order by downloadtime" % (downtime, int(news_id))
##    print sql
    news = []
    news_downtime = []
    try:
        cur.execute(sql)
        for row in cur.fetchall():
            news.append(row[0])
            news_downtime.append(util.dt2str(row[1]))
    finally:
        if conn:
            conn.close()
    return (news, news_downtime)

def getSound(category_id, downtime='', isTrain=True):
    conn = MySQLdb.connect(host='10.141.201.62', user='root', passwd='medlab', db='media', charset='utf8')
    cur = conn.cursor()
    sql = ''
    if isTrain:
        sql = "select soundid, name, downloadtimedate from sound where categoryid like '%s' and downloadtimedate != 'null' and downloadtimedate != 'un' order by downloadtimedate desc limit 3000" % (category_id+'%')
    else:
        sql = "select soundid, downloadtimedate from sound where categoryid like '%s' and length < '05:00' and length(length) = 5 and downloadtimedate between '%s'-interval 24 hour and '%s' and audiodown = '1' " % (category_id+'%', downtime, downtime)
##    print sql
    sounds = []
    soundid = []
    downloadtimedate = []
    try:
        cur.execute(sql)
        for row in cur.fetchall():
            soundid.append(row[0].encode('utf-8'))
            if isTrain:
                sounds.append(row[1])
                downloadtimedate.append(row[2].encode('utf-8'))
            else:
                downloadtimedate.append(row[1].encode('utf-8'))

    finally:
        if conn:
            conn.close()
    if isTrain:
        return (soundid, sounds, downloadtimedate)
    else:
        return (soundid, downloadtimedate)

def insPromoted(categoryid, soundid, num):
    conn = MySQLdb.connect(host='10.141.201.62', user='root', passwd='medlab', db='media', charset='utf8')
    cur = conn.cursor()
    sql = '''insert into news_promoted(categoryid, promotednum ,promotednews, updatetime) values('%s', '%d', '%s', now())''' % (categoryid, int(num), soundid)
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except:
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
