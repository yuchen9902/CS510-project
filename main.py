from model import unigram, bigram, multinomial
import json
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold, train_test_split


def compute_accuracies(predicted_label, test_label):
    count = 0
    for i in range(len(predicted_label)):
        if predicted_label[i] == test_label[i]:
            count += 1
    accuracy = count / len(predicted_label)
    cm = confusion_matrix(test_label, predicted_label)
    true_negative, false_positive, false_negative, true_positive = cm.ravel()
    return accuracy, false_positive, false_negative, true_positive, true_negative


def onefold_estimation(data_set, data_label, uni=True, bi=False, multi=False):
    data_set = data_set[:50000] + data_set[-50000:]
    data_label = data_label[:50000] + data_label[-50000:]
    train_set, test_set, train_label, test_label = train_test_split(data_set, data_label,
                                                                    test_size=0.3, random_state=12345)

    # predict label and calculate the accuracy
    if uni:
        predict_label = unigram(train_set, train_label, test_set)
    elif bi:
        predict_label = bigram(train_set, train_label, test_set)
    elif multi:
        predict_label = multinomial(train_set, train_label, test_set, change_type=False)
    print(classification_report(list(test_label), predict_label))
    return 0


def nfold_estimation(data_set, data_label, uni=True, bi=False, multi=False):
    # 10 fold, pick 1/10 data as test data
    kf = KFold(n_splits=10, random_state=12345, shuffle=True)
    acc_list = []
    for train_index, test_index in kf.split(data_set):
        train_set = np.array(data_set, dtype=object)[train_index]
        test_set = np.array(data_set, dtype=object)[test_index]
        train_label = np.array(data_label, dtype=object)[train_index]
        test_label = np.array(data_label, dtype=object)[test_index]

        # predict label and calculate the accuracy
        if uni:
            predict_label = unigram(train_set, train_label, test_set)
        elif bi:
            predict_label = bigram(train_set, train_label, test_set)
        elif multi:
            predict_label = multinomial(train_set, train_label, test_set, change_type=True)
        acc, _, _, _, _ = compute_accuracies(predict_label, list(test_label))
        print(acc)
        acc_list.append(acc)
    acc = np.mean(acc_list)
    print("===== mean accuracy is %f =====" % (np.mean(acc_list)))
    return acc


def main(onefold=True, uni=True, bi=True, multi=True):
    file_data = open('processed_data/data.json', 'r')
    data_set = json.load(file_data)
    file_label = open('processed_data/label.json', 'r')
    data_label = json.load(file_label)

    if onefold:
        if uni:
            print("===== one fold, unigram =====")
            onefold_estimation(data_set, data_label)
        elif bi:
            print("===== one fold, bigram =====")
            onefold_estimation(data_set, data_label, False, True, False)
        elif multi:
            print("===== one fold, multinomial =====")
            onefold_estimation(data_set, data_label, False, False, True)
    else:
        if uni:
            print("===== nfold, unigram =====")
            nfold_estimation(data_set, data_label)
        elif bi:
            print("===== nfold, bigram =====")
            nfold_estimation(data_set, data_label, False, True, False)
        elif multi:
            print("===== nfold, multinomial =====")
            nfold_estimation(data_set, data_label, False, False, True)


if __name__ == "__main__":
    main(False, False, False, True)
