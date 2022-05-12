import pandas as pd
import os
import json
import re
import random


PATH = "./training_t2/TRAINING_DATA/"
DROP = ['ID', 'INFO']
LABEL_DICT = {'pos': 1, 'neg': 0}
global pos_count
global neg_count


sample_dict = {'2017': 49692, '2018': 40744}


# extract raw data from xml
def xml_to_json(year, label, curr_dict):
    subject_count = 0
    curr_path = PATH + year + "_cases/" + label + "/"
    dir_list = os.listdir(curr_path)
    subject_count += len(dir_list)

    context_count = 0
    for xml in dir_list:
        xml_path = curr_path + xml
        df = pd.read_xml(open(xml_path, "r").read())

        dropped = df.drop(DROP, axis=1)
        dropped.dropna(how="all", inplace=True)
        context_count += dropped.shape[0]
        result = dropped.to_json(orient="records")
        parsed = json.loads(result)

        subject_idx = xml.split(".")[0]
        subject_id = subject_idx + "_" + year
        curr_dict[subject_id] = parsed
    print("number of " + label + " subjects in " + year + ":", subject_count)
    print("pieces of context:", context_count)
    print("===================================================")


# extract only title and text
def get_text(year, label):
    subject_count = 0
    curr_path = PATH + year + "_cases/" + label + "/"
    dir_list = os.listdir(curr_path)
    subject_count += len(dir_list)

    train_data = []
    train_label = []

    context_count = 0
    for xml in dir_list:
        if xml == ".DS_Store":
            continue
        xml_path = curr_path + xml
        df = pd.read_xml(open(xml_path, "r").read())

        df.dropna(how="all", inplace=True)

        df['TITLE'] = df['TITLE'].fillna('')
        df['TEXT'] = df['TEXT'].fillna('')

        agg = df[['TITLE', 'TEXT']].agg(' '.join, axis=1)
        title_list = agg.to_list()
        context_count += len(title_list)
        for l in title_list:
            l = l.strip()
            clean_text = re.sub(r"[^A-Za-z0-9\s]+", "", l)
            clean_text = clean_text.replace("\n", " ")
            train_data.append(list(filter(None, clean_text.split())))
            train_label.append(LABEL_DICT[label])

    print("equal? ", len(train_data) == len(train_label))
    print("number of " + label + " subjects in " + year + ":", subject_count)
    print("pieces of content:", context_count)
    print("===================================================")
    return train_data, train_label


def get_json():
    pos = dict()
    neg = dict()
    for i in range(2017, 2019):
        xml_to_json(year=str(i), label="pos", curr_dict=pos)
        xml_to_json(year=str(i), label="neg", curr_dict=neg)

    with open('pos.json', 'w') as f:
        json.dump(pos, f, indent=4)

    with open('neg.json', 'w') as f:
        json.dump(neg, f, indent=4)


def sample_data(year, train_data, train_label):
    random_indices = random.sample(range(0, len(train_data)), sample_dict[year])
    data = [train_data[i] for i in random_indices]
    label = [train_label[i] for i in random_indices]
    return data, label


def get_train_set():
    train_data = []
    train_label = []
    for i in range(2017, 2019):
        for k in ['pos', 'neg']:
            data, label = get_text(year=str(i), label=k)
            sampled_data, sampled_label = sample_data(str(i), data, label)
            train_data += sampled_data
            train_label += sampled_label
            print("#######################")
            print("year: ", i, "label: ", k)
            print("count: ", len(sampled_data))
            print("#######################")

    with open('processed_data/data.json', 'w') as f:
        json.dump(train_data, f, indent=4)
    with open('processed_data/label.json', 'w') as f:
        json.dump(train_label, f, indent=4)
    return train_data, train_label


def main():
    # get_json()
    train_data, train_label = get_train_set()


if __name__ == "__main__":
    main()
