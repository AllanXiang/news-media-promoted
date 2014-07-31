# -*- coding: utf-8 -*-
import MySQLdb
import util

def getNews(news_category_id, downtime):
    '''
    查询24小时内新闻
    '''
    conn = MySQLdb.connect(host='10.141.201.62', user='root', passwd='medlab', db='media', charset='utf8')
    cur = conn.cursor()
    sql = "select contents,downloadtime from news where downloadtime between '%s'-interval 24 hour and '%s' and categoryid = '%d'" % (downtime, downtime, int(news_category_id))
##    print sql
    
    news = []
    try:
        cur.execute(sql)
        for row in cur.fetchall():
            news.append(( row[0], util.dt2str(row[1]) ))
    finally:
        if conn:
            conn.close()
    return news

def getSound(category_id, downtime1, downtime2):
    conn = MySQLdb.connect(host='10.141.201.62', user='root', passwd='medlab', db='media', charset='utf8')
    cur = conn.cursor()
    
    sql = "select soundid, name, downtime from sound where downtime between '%s' and '%s' " % (downtime1, downtime2)

    tmp = ' or '.join(["categoryid like '%s'" % (x+'%') for x in category_id])
    sql += "and audiodown = '1' and (" + tmp + ") and length < '05:00' and length(length) = 5 order by downtime desc" 

##    print sql
    sounds = []
    # soundid = []
    # downloadtimedate = []
    try:
        cur.execute(sql)
        for row in cur.fetchall():
            # soundid.append(row[0].encode('utf-8'))
            sounds.append(( row[0].encode('utf-8'), row[1], util.dt2str(row[2]) ))
            # downloadtimedate.append(util.dt2str(row[2]))

    finally:
        if conn:
            conn.close()
    return sounds

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
