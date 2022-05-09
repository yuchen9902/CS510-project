import math
import numpy as np 
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

def unigram(train_set, train_labels, dev_set, smoothing_parameter=0.3, pos_prior=0.8):
    """
    train_set - [['like','this','movie'], ['i','fall','asleep']]
    train_labels - List of labels corresponding with train_set
    """
    dic_pos = {}
    dic_neg = {}
    negative_count = 0
    positive_count = 0

    for i in range(len(train_set)):
        if train_labels[i] == 1:
            positive_count += len(train_set[i])
        else:
            negative_count += len(train_set[i])

        for j in range(len(train_set[i])):
            if train_labels[i] == 1:
                dic_pos[train_set[i][j]] = dic_pos.get(train_set[i][j], 0) + 1
            else:
                dic_neg[train_set[i][j]] = dic_neg.get(train_set[i][j], 0) + 1

    pos_V = len(dic_pos)
    neg_V = len(dic_neg)

    punk_pos = math.log(smoothing_parameter / (positive_count + smoothing_parameter * (pos_V + 1)))
    punk_neg = math.log(smoothing_parameter / (negative_count + smoothing_parameter * (neg_V + 1)))

    res = []
    for l in dev_set:
        pos_total = 0
        neg_total = 0

        for word in l:
            if word in dic_pos:
                temp = (dic_pos[word] + smoothing_parameter) / (positive_count + smoothing_parameter * (pos_V + 1))
                pos_total += math.log(temp)
            else:
                pos_total += punk_pos

            if word in dic_neg:
                temp = (dic_neg[word] + smoothing_parameter) / (negative_count + smoothing_parameter * (neg_V + 1))
                neg_total += math.log(temp)
            else:
                neg_total += punk_neg

        pos_total += math.log(pos_prior)
        neg_total += math.log(1 - math.log(pos_prior))

        if pos_total >= neg_total:
            res.append(1)
        else:
            res.append(0)
    return res


def bigram(train_set, train_labels, dev_set, unigram_smoothing_parameter=0.035, bigram_smoothing_parameter=0.02,
           bigram_lambda=0.08, pos_prior=0.8):
    """
    train_set -  [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    """
    # unigram
    dic_pos = {}
    dic_neg = {}
    negative_count = 0
    positive_count = 0

    for i in range(len(train_set)):
        if train_labels[i] == 1:
            positive_count += len(train_set[i])
        else:
            negative_count += len(train_set[i])

        for j in range(len(train_set[i])):
            if train_labels[i] == 1:
                dic_pos[train_set[i][j]] = dic_pos.get(train_set[i][j], 0) + 1
            else:
                dic_neg[train_set[i][j]] = dic_neg.get(train_set[i][j], 0) + 1

    pos_V = len(dic_pos)
    neg_V = len(dic_neg)
    punk_pos = math.log(unigram_smoothing_parameter / (positive_count + unigram_smoothing_parameter * (pos_V + 1)))
    punk_neg = math.log(unigram_smoothing_parameter / (negative_count + unigram_smoothing_parameter * (neg_V + 1)))

    # bigram
    dic_pos_bi = {}
    dic_neg_bi = {}
    negative_count_bi = 0
    positive_count_bi = 0

    for i in range(len(train_set)):
        if train_labels[i] == 1:
            positive_count_bi += len(train_set[i]) - 1
        else:
            negative_count_bi += len(train_set[i]) - 1

        for j in range(len(train_set[i]) - 1):
            st = train_set[i][j] + train_set[i][j + 1]
            if train_labels[i] == 1:
                if st not in dic_pos_bi:
                    dic_pos_bi[st] = 1
                else:
                    dic_pos_bi[st] += 1
            else:
                if st not in dic_neg_bi:
                    dic_neg_bi[st] = 1
                else:
                    dic_neg_bi[st] += 1

    pos_V_bi = len(dic_pos_bi)
    neg_V_bi = len(dic_neg_bi)
    punk_pos_bi = math.log(
        bigram_smoothing_parameter / (positive_count_bi + bigram_smoothing_parameter * (pos_V_bi + 1)))
    punk_neg_bi = math.log(
        bigram_smoothing_parameter / (negative_count_bi + bigram_smoothing_parameter * (neg_V_bi + 1)))

    # calculation
    res = []
    for l in dev_set:
        pos_total = math.log(pos_prior)
        neg_total = math.log(1 - math.log(pos_prior))
        pos_total_bi = math.log(pos_prior)
        neg_total_bi = math.log(1 - math.log(pos_prior))

        for word in l:
            if word in dic_pos:
                t = (dic_pos[word] + unigram_smoothing_parameter) / (
                            positive_count + unigram_smoothing_parameter * (pos_V + 1))
                pos_total += math.log(t)
            else:
                pos_total += punk_pos

            if word in dic_neg:
                t = (dic_neg[word] + unigram_smoothing_parameter) / (
                            negative_count + unigram_smoothing_parameter * (neg_V + 1))
                neg_total += math.log(t)
            else:
                neg_total += punk_neg

        for i in range(len(l) - 1):
            st = l[i] + l[i + 1]
            if st in dic_pos_bi:
                t = (dic_pos_bi[st] + bigram_smoothing_parameter) / (
                            positive_count_bi + bigram_smoothing_parameter * (pos_V_bi + 1))
                pos_total_bi += math.log(t)
            else:
                pos_total_bi += punk_pos_bi

            if st in dic_neg_bi:
                t = (dic_neg_bi[st] + bigram_smoothing_parameter) / (
                            negative_count_bi + bigram_smoothing_parameter * (neg_V_bi + 1))
                neg_total_bi += math.log(t)
            else:
                neg_total_bi += punk_neg_bi

        pos = (1 - bigram_lambda) * pos_total + bigram_lambda * pos_total_bi
        neg = (1 - bigram_lambda) * neg_total + bigram_lambda * neg_total_bi

        if pos >= neg:
            res.append(1)
        else:
            res.append(0)
    return res
    

def multinomial(train_set, train_labels, test_set, change_type=False):
    if change_type:
        train_labels = train_labels.astype('int')
    tf_idf = TfidfVectorizer()
    #applying tf idf to training data
    X_train_tf = tf_idf.fit_transform(train_set)
    #applying tf idf to training data
    X_train_tf = tf_idf.transform(train_set)
    X_test_tf = tf_idf.transform(test_set)
    naive_bayes_classifier = MultinomialNB()
    naive_bayes_classifier.fit(X_train_tf, train_labels)
    y_pred = naive_bayes_classifier.predict(X_test_tf)

    return y_pred

