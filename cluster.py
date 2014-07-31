# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
    
def news_cluster(news, threshold, now):
    docs, scores = zip(*news)
    clusters = train(docs, threshold)

    selected = []
    len_clusters = len(clusters)
    # fp = open('log/'+ now +'/news_cluster', 'w')
    for i in range(len_clusters):
        cluster = clusters[i]
        # throw len(cluster) == 1 
        # if len(cluster) == 1:
        #     continue
        cluster.sort(key=lambda item: -news[item][1])

        tot = 0
        for item in cluster:
            tot += news[item][1]

            # ss = news[item][0]+'\t'+str(news[item][1])
            # fp.write(ss.encode('utf-8'))
            # fp.write('\n')
        
        selected.append( (news[cluster[0]][0], tot) )
        # fp.write('\n')
    
    print 'selected news size:',len(selected)
    selected.sort(key=lambda item: -item[1])

    # fp.write('\n\ntot\n')
    # for item in selected:
    #     ss = item[0]+'\t'+str(item[1])
    #     fp.write(ss.encode('utf-8'))
    #     fp.write('\n')

    # fp.close()
    return selected

def train(documents, threshold):
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

    
def sound_cluster(sounds, threshold, now):
    ids, docs, scores = zip(*sounds)
    clusters = train(docs, threshold)
    selected = []
    
    len_clusters = len(clusters)
    # fp = open('log/'+ now +'/sound_cluster', 'w')
    for i in range(len_clusters):
        cluster = clusters[i]
        if len(cluster) < 2:
            continue
        cluster.sort(key=lambda item: sounds[item][2], reverse=True)

        # for item in cluster:
        #     ss = sounds[item][0]+'\t'+sounds[item][1]+'\t'+sounds[item][2]
        #     fp.write(ss.encode('utf-8'))
        #     fp.write('\n')
        
        selected.append(sounds[cluster[0]])
        
        # fp.write('\n')
    # fp.close()

    selected.sort(key=lambda item: item[2], reverse=True)
    print 'selected sound size:',len(selected)
    return selected
