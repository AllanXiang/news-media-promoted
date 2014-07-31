# -*- coding: utf-8 -*-
import jieba
import util
import json

point = [10,8,7,6,5,4,3,2,1,1]
stopwords = util.StopWords()

def getPoint(place, downtime , now):
    '''
    两小时内时间权重因子为3
    '''
    tmp = util.sub_time(now, downtime)
    score = 1
    if tmp < 2.0:
        score = 3
    if place < 10:
        return score*point[place]
    else:
        return score


def pre_all(news_corpus, sounds_corpus, now):
    """
    pre corpus
    """
    news = pre_news(news_corpus, now)
    sounds = pre_sound(sounds_corpus)
    # print 'pre done'
    return (news, sounds)

def pre_news(news_corpus, now):
    news_seg = []
    vote = []
    vote_time = []
    news2index = {}
    index = 0
    for line in news_corpus:
        s = json.loads(line[0])
        for j, doc in enumerate(s):
            k = news2index.get(doc, -1)
            if k == -1:
                news2index[doc] = index;
                index = index+1
                
                seg_list = jieba.cut(''.join(doc.split()))
                to_write = ''
                for word in seg_list:
                    if word.encode('utf-8') not in stopwords:
                        to_write += word+' '
                news_seg.append(to_write)
                
                vote.append(getPoint(j, line[1], now))
                vote_time.append(line[1])
            else:
                vote[news2index[doc]] += getPoint(j, vote_time[k], now)
    print '24 hour news_len:', len(news_seg)

    news = []
    for i, item in enumerate(vote):
        news.append(( news_seg[i], HN_score(item, util.sub_time(now, vote_time[i])) ))
       
##    排序输出news分数
##    tmp = zip(news_seg, news_scores, vote, vote_time)
##    tmp.sort(key=lambda item: item[1], reverse=True)
##    fp = open('log/'+ now +'/news_scores', 'a')
##    for item in tmp:
##        sss=item[0]+'\t'+str(item[1])+'\t'+str(item[2])+'\t'+item[3]+'\n'
##        fp.write(sss.encode('utf-8'))
##    fp.close()
    
    return news

def HN_score(P, T, G=1.8):
    return (P-1) / pow((T+2), G)
##    return log10(P) / pow((T+2), G)

def pre_sound(sounds_corpus):
    sounds = []
    for line in sounds_corpus:
        seg_list = jieba.cut(''.join(line[1].split()))
        towrite = ''
        for word in seg_list: 
            if word.encode('utf-8') not in stopwords:
                towrite += word+' '
        sounds.append(( line[0], towrite, line[2] ))

    return sounds
