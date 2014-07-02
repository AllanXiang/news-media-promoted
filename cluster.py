# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
    
def news_cluster(documents, news_scores, threshold, now):

    clusters = train(documents, news_scores, threshold)

    selected = []
    len_clusters = len(clusters)
##    fp = open('log/'+ now +'/news_cluster', 'a')
    for i in range(len_clusters):
        cluster = clusters[i]
        cluster.sort(key=lambda item: -news_scores[item])

##        for item in cluster:
##            ss = documents[item]+'\t'+str(news_scores[item])
##            fp.write(ss.encode('utf-8'))
##            fp.write('\n')
        
        selected.append(documents[cluster[0]])

##        fp.write('\n')
##    fp.close()
    print 'selected news size:',len(selected)
    return selected

def train(documents, news_scores, threshold):
    texts = [[word for word in document.split()] for document in documents]
    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    index = similarities.MatrixSimilarity(corpus_tfidf)
    matrix_cos = []
    for i in corpus_tfidf:
        matrix_cos.append(index[i])

    matrix_len = len(matrix_cos)
    vis = [0]*matrix_len
    clusters = []
    for i in range(matrix_len):
        if vis[i] == 1:
            continue
        vis[i] = 1
        cluster = [i]
        for j in range(i+1, matrix_len):
            if vis[j] == 0 and matrix_cos[i][j] > threshold:
                vis[j] = 1
                cluster.append(j)
        clusters.append(cluster)

    return clusters

    
def sound_cluster(ids, documents, news_scores, threshold, now):

    clusters = train(documents, news_scores, threshold)
    selected_id = []
    selected_downtime = []
    
    len_clusters = len(clusters)
##    fp = open('log/'+ now +'/sound_cluster', 'a')
    for i in range(len_clusters):
        cluster = clusters[i]
        cluster.sort(key=lambda item: news_scores[item], reverse=True)

##        for item in cluster:
##            ss = ids[item]+'\t'+documents[item]+'\t'+news_scores[item]
##            fp.write(ss.encode('utf-8'))
##            fp.write('\n')
        
        selected_id.append(ids[cluster[0]])
        selected_downtime.append(news_scores[cluster[0]])
        
##        fp.write('\n')
##    fp.close()
    print 'selected sound size:',len(selected_id)
    return (selected_id, selected_downtime)
