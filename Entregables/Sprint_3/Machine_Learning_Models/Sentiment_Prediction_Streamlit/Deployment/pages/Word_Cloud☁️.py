import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

import datetime
import re
import base64

import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

#https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
#https://towardsdatascience.com/creating-an-interactive-datetime-filter-with-pandas-and-streamlit-156e1ea12e90

st. set_page_config(layout="wide")

st.title("Word Cloud")
st.markdown("In this page you can see the word cloud generates with the most frequent words")

if 'Dataset' not in st.session_state:
	st.write("Please let the page 'Welcome! 👋' load first")
else:

	Dataset = st.session_state['Dataset']
	def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
		"""
		Adds a UI on top of a dataframe to let viewers filter columns

		Args:
		df (pd.DataFrame): Original dataframe

		Returns:
		pd.DataFrame: Filtered dataframe
		"""
		modify = st.checkbox("Add filters")

		if not modify:
		    return df 

		Dataset_filtered = df.copy()

		# Try to convert datetimes into a standard format (datetime, no timezone)
		for col in Dataset_filtered.columns:
			if is_object_dtype(Dataset_filtered[col]):
				try:
					Dataset_filtered[col] = pd.to_datetime(Dataset_filtered[col])
				except Exception:
					pass

			if is_datetime64_any_dtype(Dataset_filtered[col]):
				Dataset_filtered[col] = Dataset_filtered[col].dt.tz_localize(None)        
			
		modification_container = st.container()
		with modification_container:
			to_filter_columns = st.multiselect("Filter dataframe on", Dataset_filtered.columns)	
			for column in to_filter_columns:
				left, right = st.columns((1, 20))
				# Treat columns with < 10 unique values as categorical
				if is_categorical_dtype(Dataset_filtered[column]) or Dataset_filtered[column].nunique() < 10:
					user_cat_input = right.multiselect(
					    f"Values for {column}",
					    Dataset_filtered[column].unique(),
					    default=list(Dataset_filtered[column].unique()),
					)
					Dataset_filtered = Dataset_filtered[Dataset_filtered[column].isin(user_cat_input)]
				elif is_numeric_dtype(Dataset_filtered[column]):
					_min = float(Dataset_filtered[column].min())
					_max = float(Dataset_filtered[column].max())
					step = (_max - _min) / 100
					user_num_input = right.slider(
					    f"Values for {column}",
					    min_value=_min,
					    max_value=_max,
					    value=(_min, _max),
					    step=step,
					)
					Dataset_filtered = Dataset_filtered[Dataset_filtered[column].between(*user_num_input)]
				elif is_datetime64_any_dtype(Dataset_filtered[column]):
					user_date_input = right.date_input(
					    f"Values for {column}",
					    value=(
						Dataset_filtered[column].min(),
						Dataset_filtered[column].max(),
					    ),
					)
					if len(user_date_input) == 2:
						    user_date_input = tuple(map(pd.to_datetime, user_date_input))
						    start_date, end_date = user_date_input
						    Dataset_filtered = Dataset_filtered.loc[Dataset_filtered[column].between(start_date, end_date)]
				else:
					user_text_input = right.text_input(
					    f"Substring or regex in {column}",
					)
					if user_text_input:
						Dataset_filtered = Dataset_filtered[Dataset_filtered[column].astype(str).str.contains(user_text_input)]

			return Dataset_filtered

        
        

	

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


	st.set_option('deprecation.showPyplotGlobalUse', False)


	Dataset_filter= filter_dataframe(Dataset)

	st.pyplot(WordCloudPlott(Dataset_filter.loc[:,'cleaned_review'], title='Word Cloud Portuguese'))

