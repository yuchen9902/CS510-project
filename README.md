# CS510-project

## MODEL TRAINING
### data preprocessing
Since it is a classification problem, we use the same amount of positive and negative data to train our model.
We removed stop words and punctuation words, and lemmetized based on sentences. 

Run preprocess.py to process data. Data will be saved in folder "processed_data".

### training
Run main.py to train model. Model will be saved into "finalized_model.sav" and "tfidf_vectorizer.sav"

## Website
Run api.py to start server.