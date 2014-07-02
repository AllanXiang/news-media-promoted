# -*- coding: utf-8 -*-
import MySQLdb
import util

def getNews(news_id, downtime):
    '''
    查询24小时内新闻
    '''
    conn = MySQLdb.connect(host='10.141.201.62', user='root', passwd='medlab', db='media', charset='utf8')
    cur = conn.cursor()
    sql = "select contents,downloadtime from news where downloadtime >= '%s'-interval 24 hour and categoryid = '%d'" % (downtime, int(news_id))
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

def getSound(category_id, downtime):
    conn = MySQLdb.connect(host='10.141.201.62', user='root', passwd='medlab', db='media', charset='utf8')
    cur = conn.cursor()
    
    sql = "select soundid, name, downloadtimedate from sound where downloadtimedate between '%s'-interval 72 hour and '%s' " % (downtime, downtime)

    tmp = ' or '.join(["categoryid like '%s'" % (x+'%') for x in category_id])
    sql += "and audiodown = '1' and (" + tmp + ") and length < '05:00' and length(length) = 5 order by downloadtimedate desc" 

##    print sql
    sounds = []
    soundid = []
    downloadtimedate = []
    try:
        cur.execute(sql)
        for row in cur.fetchall():
            soundid.append(row[0].encode('utf-8'))
            sounds.append(row[1])
            downloadtimedate.append(row[2].encode('utf-8'))

    finally:
        if conn:
            conn.close()
    return (soundid, sounds, downloadtimedate)

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
