import streamlit as st
import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt


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

from wordcloud import WordCloud, STOPWORDS
from nltk.probability import FreqDist

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
st.markdown("Here you can upload your reviews dataset to know how your users are responding to sales")

def WordCloudPlott(dataset_words, title):
# Python program to generate WordCloud translated
  comment_words = ''
  stopwords = set(STOPWORDS)


  # iterate through the csv file
  for val in dataset_words.values:
      
      # typecaste each val to string
      val = str(val)
  
      # split the value
      tokens = val.split()
      
      # Converts each token into lowercase
      for i in range(len(tokens)):
          tokens[i] = tokens[i].lower()
      comment_words += " ".join(tokens)+" "


  
  wordcloud = WordCloud(width = 800, height = 800,
                  background_color ='black',
                  stopwords = stopwords,
                  min_font_size = 10).generate(comment_words)
  
  # plot the WordCloud image                      
  plt.figure(figsize = (8, 8), facecolor = None)
  plt.title(title)
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.tight_layout(pad = 0)
  
  plt.show()

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
    
def _get_freq_dist_list(dataset_words):
    ls = []
    # Python program to generate WordCloud translated
    comment_words = ''
    stopwords = set(STOPWORDS)


    # iterate through the csv file
    for val in dataset_words.values:
        
        # typecaste each val to string
        val = str(val)
    
        # split the value
        tokens = val.split()
        for tk_line in tokens:
          #for word in tk_line:
          ls.append(tk_line)

    return ls
    
def Plot_Common_words(dataset_words, title, lang='portuguese'):
    # Frequency Distribution on training dataset
    fd_list = _get_freq_dist_list(dataset_words)
    fdist = FreqDist(fd_list)
    #print(fdist)

    # most common words
    most_common = fdist.most_common(25)
    #print(most_common)

    # most uncommon words (words that appear once)
    most_uncommon = fdist.hapaxes()
    #print(most_uncommon[0:30])

    # find the word occuring max number of times
    #print(fdist.max())
    data={'Word' : [k for k, v in most_common],
          'Count' : [v for k, v in most_common]}
    series=pd.DataFrame(data)
    if lang=='english':
      series.Word.iloc[:30]= series.Word.iloc[:30].apply(lambda x: tss.reverso(x, from_language='pt', to_language='en', if_ignore_empty_query=True, if_ignore_limit_of_length=True, limit_of_length=5000))

    #Plot:
    fig = plt.figure(figsize = (20,8), facecolor='black')
    sns.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})
    plot = sns.barplot(x  = series.iloc[:30].Word, y = series.iloc[:30].Count, palette= "jet_r")#, backcolor='black')

    for item in plot.get_xticklabels():
        item.set_rotation(20)
        item.set_size(14)
        item.set_color('white')
   
    for item in plot.get_yticklabels():
        item.set_color('white')
        item.set_size(14)

    plt.title(title+'\n', fontsize= 22, color='white')
    plt.show()
    

model = joblib.load("sentiment_model_pt_pipeline.pkl")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    

    dataframe.dropna(inplace=True)
    dataframe.reset_index(inplace=True, drop=True)
    dataframe=dataframe[:100]

    sentiments = {0: "Negative", 1: "Positive"}   
    dataframe["review_comment_message"] = dataframe["review_comment_message"].astype("string")
    dataframe["cleaned_review"] = dataframe["review_comment_message"].apply(text_cleaning)
#    dataframe["cleaned_review"] = text_cleaning(dataframe["review_comment_message"])
#    X_input = vectorizer.transform(dataframe["clean"])
    dataframe["Review_prediction"] = model.predict(dataframe["cleaned_review"])
    dataframe["Review_sentiment"] = np.where(dataframe.loc[:,('Review_prediction')] ==1, 'Positive', 'Negative')
    # output dictionary

    




st.set_option('deprecation.showPyplotGlobalUse', False)
if uploaded_file is not None:
    if st.button('Display Cloud Word'):

        st.pyplot(WordCloudPlott(dataframe.loc[:,'cleaned_review'], title='Word Cloud Portuguese'))

    if st.button('Display Word Histogram'):
    	st.pyplot(Plot_Common_words(dataframe.loc[:,'cleaned_review'],  title='Common words portuguese'))

    if st.button('Display dataframe with Prediction on sentiment'):
    	st.write(dataframe)
    


