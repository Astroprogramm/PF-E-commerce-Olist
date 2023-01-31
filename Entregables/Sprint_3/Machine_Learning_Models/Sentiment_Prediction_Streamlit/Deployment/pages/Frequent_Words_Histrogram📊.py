import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

from nltk.probability import FreqDist
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st. set_page_config(layout="wide")

st.title("Top 25 most frequent words")
st.markdown("In this page you can see the histogram with the top 25 most frequent words")

if 'Dataset' not in st.session_state:
	st.write("Please let the page 'Welcome! 👋' load first")
	
#elif Dataset in st.session_state:
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

	def Plot_Common_words(dataset_words, title):
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

		#Plot:
		fig = plt.figure(figsize = (20,8), facecolor='black')
		sns.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})
		plot = sns.barplot(x  = series.iloc[:25].Word, y = series.iloc[:25].Count, palette= "jet_r")#, backcolor='black')

		for item in plot.get_xticklabels():
			item.set_rotation(20)
			item.set_size(14)
			item.set_color('white')

		for item in plot.get_yticklabels():
			item.set_color('white')
			item.set_size(14)

		plt.title(title+'\n', fontsize= 22, color='white')
		plt.show()



	def _get_freq_dist_list(dataset_words):
		ls = []

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


	Dataset = st.session_state['Dataset'] 
	Dataset_filter= filter_dataframe(Dataset)

	st.set_option('deprecation.showPyplotGlobalUse', False)

	st.pyplot(Plot_Common_words(Dataset_filter.loc[:,'cleaned_review'],  title='Common words portuguese'))
