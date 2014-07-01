# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
    
def cos_tfidf(documents, news_scores, threshold):

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
##    clusters.sort(key=lambda item: -len(item))

    selected = []
    len_clusters = len(clusters)
##    fp_output = open('/home/xzy/PythonFiles/FM/log/cluster', 'w')
    
    for i in range(len_clusters):
        cluster = clusters[i]
        cluster.sort(key=lambda item: -news_scores[item])
##        if len(cluster) < 2:
##            continue
##        for item in cluster:
##            fp_output.write(documents[item].encode('utf-8')+'\n')
##        fp_output.write('\n')
        
        selected.append(documents[cluster[0]])
 
##    fp_output.close()
    print 'cluster down'
    print 'selected size:',len(selected)
    return selected


    
