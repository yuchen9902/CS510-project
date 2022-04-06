from model import unigram
import json
import numpy as np
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


def onefold_estimation(data_set, data_label):
    train_set, test_set, train_label, test_label = train_test_split(data_set, data_label,
                                                                    test_size=0.3, random_state=12345)
    # predict label and calculate the accuracy
    predict_label = unigram(train_set, train_label, test_set)
    acc, fp, _, _, _ = compute_accuracies(predict_label, list(test_label))
    print("===== accuracy is %f =====" % acc)
    print("===== false_positive is %d ===== " % fp)
    return acc


def nfold_estimation(data_set, data_label):
    # 10 fold, pick 1/10 data as test data
    kf = KFold(n_splits=10, random_state=12345, shuffle=True)
    acc_list = []
    for train_index, test_index in kf.split(data_set):
        train_set = np.array(data_set, dtype=object)[train_index]
        test_set = np.array(data_set, dtype=object)[test_index]
        train_label = np.array(data_label, dtype=object)[train_index]
        test_label = np.array(data_label, dtype=object)[test_index]

        # predict label and calculate the accuracy
        predict_label = unigram(train_set, train_label, test_set)
        acc, _, _, _, _ = compute_accuracies(predict_label, list(test_label))
        print(acc)
        acc_list.append(acc)
    acc = np.mean(acc_list)
    print("===== mean accuracy is %f =====" % (np.mean(acc_list)))
    return acc


def main(nfold=False):
    file_data = open('data.json', 'r')
    data_set = json.load(file_data)
    file_label = open('label.json', 'r')
    data_label = json.load(file_label)
    print("===== finish loading data =====")

    if nfold:
        nfold_estimation(data_set, data_label)
    else:
        onefold_estimation(data_set, data_label)


if __name__ == "__main__":
    main()
