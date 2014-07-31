# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
import util
import json

threshold = 0.4
threshold_big = 0.5

def start(news_selected, sounds_selected, sounds, now, file_name, sounds_cluster):
    ids, docs, downtimes = zip(*sounds)
    ids_sel, docs_sel, downtimes_sel = zip(*sounds_selected)
    dic, tfidf, index = train(docs)
    finds = find(news_selected, dic, tfidf, index, sounds, now, file_name, ids_sel)

    num = len(finds)
    print 'match size:', num
    if num < 100:

        fp_find = open('log/'+now+'/'+file_name, 'a')
        fp_find.write('add newest sound to fulfill req\n')
        for item in sounds_cluster[:110-num]:
            if item[0] not in finds:
                to_write = item[0]+'\t'+item[1]+'\t'+item[2]+'\n'
                fp_find.write(to_write.encode('utf-8'))
                finds.append(item[0])

        fp_find.close()

        num = len(finds)
        print 'tot find:', num
        
    return (num, json.dumps(finds))    

    
def train(documents):
    
    texts = [[word for word in document.split()] for document in documents]
    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    
    index = similarities.MatrixSimilarity(corpus_tfidf)
##    print 'make up dic&tfidf&index'
    return (dictionary, tfidf, index)


def find(selected, dic, tfidf, index, sounds, now, file_name, ids_sel):
    res = []
    
    fp_find = open('log/'+now+'/'+file_name, 'w')
    for query in selected:
        query_bow = dic.doc2bow(query[0].split())
        query_tfidf = tfidf[query_bow]
        sims = index[query_tfidf]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        len_sort_sims = len(sort_sims)

        for i in range(len_sort_sims):
            place = sort_sims[i][0]
            simi = sort_sims[i][1]
            if simi < threshold:
                break     

            if sounds[place][0] in ids_sel:
                tmp = sounds[place]
                if (util.checktime(now, tmp[2]) or simi > threshold_big) and tmp[0] not in res:
                    res.append(tmp[0])
                    to_write = 'query: '+query[0]+'\tpoint: '+str(query[1])+'\n'
                    to_write += sounds[place][0]+'\t'+sounds[place][1]+'\t'+str(simi)+'\t'+sounds[place][2]+'\n\n'
                    fp_find.write(to_write.encode('utf-8'))
                    break

            # to_write = sounds[place][0]+'\t'+sounds[place][1]+'\t'+str(simi)+'\t'+sounds[place][2]+'\n'
            # fp_find.write(to_write.encode('utf-8'))
                
    fp_find.close()
    return res
    
