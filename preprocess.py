#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import os
import json
import re


# In[12]:


PATH = "./training_t2/TRAINING_DATA/"
DROP = ['ID', 'INFO']
LABEL_DICT = {'pos': 1, 'neg': 0}
global pos_count
global neg_count
pos_count = 0
neg_count = 0


# In[13]:


# extract raw data from xml
def xml_to_json(year, label, curr_dict):
    subject_count = 0
    curr_path = PATH + year + "_cases/" + label + "/"
    dir_list = os.listdir(curr_path)
    subject_count += len(dir_list)
    
    context_count = 0
    for xml in dir_list:
        xml_path = curr_path+xml
        df = pd.read_xml(open(xml_path, "r").read())
        
        dropped = df.drop(DROP, axis=1)
        dropped.dropna(how="all", inplace=True)
        context_count += dropped.shape[0]
        result = dropped.to_json(orient="records")
        parsed = json.loads(result)
        
        subject_idx = xml.split(".")[0]
        subject_id = subject_idx+"_"+year
        curr_dict[subject_id] = parsed
    print("number of "+label+" subjects in "+year+":", subject_count)
    print("pieces of context:", context_count)
    print("===================================================")


# In[26]:


# extract only title and text
def get_text(year, label, train_data, train_label):
    subject_count = 0
    curr_path = PATH + year + "_cases/" + label + "/"
    dir_list = os.listdir(curr_path)
    subject_count += len(dir_list)
    
    context_count = 0
    for xml in dir_list:
        if xml == ".DS_Store":
            continue
        xml_path = curr_path+xml
        df = pd.read_xml(open(xml_path, "r").read())
        
        df.dropna(how="all", inplace=True)
#         context_count += df.shape[0]

        titles = df['TITLE']
        titles.dropna(how="all", inplace=True)
        title_list = titles.to_list()
        context_count += len(title_list)
        for l in title_list:
            clean_text = re.sub(r"[^A-Za-z0-9\s]+", "", l)
            # train_data.append(clean_text.split(" "))
            train_data.append(clean_text)
            train_label.append(LABEL_DICT[label])
            
        texts = df['TEXT']
        texts.dropna(how="all", inplace=True)
        text_list = texts.to_list()
        context_count += len(text_list)
        for l in text_list:
            clean_text = re.sub(r"[^A-Za-z0-9\s]+", "", l)
            # train_data.append(clean_text.split(" "))
            train_data.append(clean_text)
            train_label.append(LABEL_DICT[label])
#         if pd.isna(df[i]['TITLE']) == False:
#             train_data.append(df['TITLE'].split(" "))
#             train_label.append(LABEL_DICT[label])
#         if pd.isna(df[i]['TEXT']) == False:
#             train_data.append(df['TEXT'].split(" "))
#             train_label.append(LABEL_DICT[label])
        
    print("number of "+label+" subjects in "+year+":", subject_count)
    print("pieces of context:", context_count)
    print("===================================================")


# In[27]:


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


# In[43]:


def get_train_set():
    train_data = []
    train_label = []
#     get_text(year="2017", label="pos", train_data=train_data, train_label=train_label)
    for i in range(2017, 2019):
        get_text(year=str(i), label="pos", train_data=train_data, train_label=train_label)
        get_text(year=str(i), label="neg", train_data=train_data, train_label=train_label)
    with open('processed_data/data.json', 'w') as f:
        json.dump(train_data, f, indent=4)
    with open('processed_data/label.json', 'w') as f:
        json.dump(train_label, f, indent=4)
    return train_data, train_label


# In[44]:


def main():
    # get_json()
    train_data, train_label = get_train_set()
#     print(len(train_data))
#     print(train_data)
#     print("================")
#     print(len(train_label))
#     print(train_label)


# In[46]:


if __name__ == "__main__":
    main()


# In[ ]:




