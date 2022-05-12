# CS510-project

# Description 
This is a web based application that can detect depression posts. The forum is for people to share posts and detect potential depression post. \
The web application is built based on Flask framework and Python.
# System requirements
1.Python 3.8+\
2.Git
# Install guidelines
## 1. Clone the repo 
```
  git clone https://github.com/yuchen9902/CS510-project.git

```
## 2. Set up environment
```
conda create --name cs510 python=3.8
conda activate cs510
conda install numpy, flask, bson, nltk, pymongo, flask_login, python-dotenv, dnspython, sklearn, pandas

```


## MODEL TRAINING
### data preprocessing
Since it is a classification problem, we use the same amount of positive and negative data to train our model.
We removed stop words and punctuation words, and lemmetized based on sentences. 

Run preprocess.py to process data. Data will be saved in folder "processed_data".

### training
Run main.py to train model. Model will be saved into "finalized_model.sav" and "tfidf_vectorizer.sav"

## Website
If you want to run the server, type the code below in your terminal.
```
  python api.py 
```
Then the server is up at : http://127.0.0.1:8000/posts
