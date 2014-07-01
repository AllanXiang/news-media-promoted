# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
import util
import json

threshold = 0.4
threshold_big = 0.6

def start(selected, sound_id, sound_downtime, train_id, train_seg, train_downtime, now, file_name):
    dic, tfidf, index = train(train_seg)
    find_id = find(selected, dic, tfidf, index, train_id, train_seg, train_downtime, now, file_name, sound_id)

    num = len(find_id)
    print 'match size:', num
    if num < 100:
        b =set(sound_id[:110-num])
        fp_find = open('log/'+now+'/'+file_name, 'a')
        fp_find.write('add newest sound to fulfill req\n')
        for i, item in enumerate(sound_id[:110-num]):
            fp_find.write(item+'\t'+sound_downtime[i]+'\n')
        fp_find.close()
        res = find_id.union(b)
        num = len(res)
        print 'tot find:', num
        return (num, json.dumps(list(res)))
    else:
        return (num, json.dumps(list(find_id)))
    

    
def train(documents):
    
    texts = [[word for word in document.split()] for document in documents]
    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    
    index = similarities.MatrixSimilarity(corpus_tfidf)
##    print 'make up dic&tfidf&index'
    return (dictionary, tfidf, index)


def find(selected, dic, tfidf, index, train_id, documents, train_downtime, now, file_name, sound_id):
    res = set()
    
    fp_find = open('log/'+now+'/'+file_name, 'w')
    for query in selected:
        query_bow = dic.doc2bow(query.split())
        query_tfidf = tfidf[query_bow]
        sims = index[query_tfidf]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        len_sort_sims = len(sort_sims)
        for i in range(len_sort_sims):
            place = sort_sims[i][0]
            simi = sort_sims[i][1]
            if simi < threshold :
                break           
            
            if train_id[place] in sound_id:
                if util.checktime(now, train_downtime[place]) or simi > threshold_big:
                    res.add(train_id[place])
                    fp_find.write('query: '+query.encode('utf-8')+'\n')
                    to_write = train_id[place]+'\t'+documents[place]+'\t'+str(simi)+'\t'+train_downtime[place]+'\n'
                    fp_find.write(to_write.encode('utf-8'))
                    fp_find.write('\n')
                    break
                
    fp_find.close()
    return res
    
