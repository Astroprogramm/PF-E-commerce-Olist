import streamlit as st
import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import time


from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB # classifier 

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
# text preprocessing modules
from string import punctuation

# text preprocessing modules
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import re #regular expression

st. set_page_config(layout="wide")

# Download dependency
for dependency in (
    "brown",
    "names",
    "wordnet",
    "averaged_perceptron_tagger",
    "universal_tagset",
    "stopwords",
    "omw-1.4",
):
    nltk.download(dependency)
    
import warnings
warnings.filterwarnings("ignore")
# seeding
np.random.seed(123)




st.title("Sentiment prediction on review messages")
st.markdown("Here the datasets will be loaded so you can visualize the predictions")

#https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
def text_cleaning(text, remove_stop_words=True, lemmatize_words=True, lang='portuguese'):
    stop_words =  stopwords.words(lang)
    # Clean the text, with the option to remove stop_words and to lemmatize word
    # Clean the text
    text = re.sub(r"[^A-Za-z0-9]", " ", str(text))
    text = re.sub(r"\'s", " ", text)
    text =  re.sub(r'http\S+',' link ', text)
    text = re.sub(r'\b\d+(?:\.\d+)?\s+', '', text) # remove numbers
        
    # Remove punctuation from text
    text = ''.join([c for c in text if c not in punctuation])
    
    # Optionally, remove stop words
    if remove_stop_words:
        text = text.split()
        text = [w for w in text if not w in stop_words]
        text = " ".join(text)
    
    # Optionally, shorten words to their stems
    if lemmatize_words:
        text = text.split()
        lemmatizer = WordNetLemmatizer() 
        lemmatized_words = [lemmatizer.lemmatize(word) for word in text]
        text = " ".join(lemmatized_words)
    # create a count vectorizer object
    
    # Return a list of words
    return(text)



def Load_datasets():
	st.write("Loading datasets...")
	my_bar = st.progress(0)

	for percent_complete in range(100):
	    time.sleep(1.4)
	    my_bar.progress(percent_complete + 1)

	Order_reviews_df = pd.read_csv("https://raw.githubusercontent.com/Astroprogramm/PF-E-commerce-Olist/master/Datasets/olist_order_reviews_dataset.csv")
	Order_items_df = pd.read_csv("https://raw.githubusercontent.com/Astroprogramm/PF-E-commerce-Olist/master/Datasets/olist_order_items_dataset.csv")
	Products_df = pd.read_csv("https://raw.githubusercontent.com/Astroprogramm/PF-E-commerce-Olist/master/Datasets/olist_products_dataset.csv")
	st.success("Datasets loaded succesfully!")


	st.write("Preparing datasets...")
	Dataset_0 = pd.merge(Order_reviews_df, Order_items_df, how='left', on='order_id', sort=False)
	Dataset = pd.merge(Dataset_0, Products_df, how='left', on='product_id', sort=False)

	Dataset.drop(columns=['product_name_lenght', 'product_description_lenght', 'product_photos_qty','product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm', 'review_answer_timestamp', 'freight_value'] , inplace=True)

	#Dropping nulls
	Dataset.dropna(subset=['review_comment_message'], inplace=True)
	Dataset.reset_index(inplace=True, drop=True)
	st.success("Datasets ready!")
	return Dataset

model = joblib.load("sentiment_model_pt_pipeline.pkl")

def Prediction():
	st.write("Generating predictions...")
	Dataset["review_comment_message"] = Dataset["review_comment_message"].astype("string")
	Dataset["cleaned_review"] = Dataset["review_comment_message"].apply(text_cleaning)

	Dataset["Review_prediction"] = model.predict(Dataset["cleaned_review"])
	Dataset["Review_sentiment"] = np.where(Dataset.loc[:,('Review_prediction')] ==1, 'Positive', 'Negative')
	st.success("Predictions ready!")
	return Dataset


Dataset = Load_datasets()
Predictions = Prediction()
st.write("Now you can go to the other pages and visualize the results 😄")

if 'Dataset' not in st.session_state:
	st.session_state['Dataset'] = Dataset


		



