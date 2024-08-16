import streamlit as st
import pandas as pd
import textrazor
import requests
from bs4 import BeautifulSoup
import plotly.express as px
import numpy as np

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# TextRazor details
textrazor.api_key = st.secrets['API_KEY']

client = textrazor.TextRazor(extractors=["entities", "topics"])
client.set_classifiers(["textrazor_newscodes"])
client.set_do_compression(do_compression=True)
account_manager = textrazor.AccountManager()

# Graph plot function
def plot_result(top_topics, scores):
	top_topics = np.array(top_topics)
	scores = np.array(scores)
	scores *= 100
	fig = px.bar(x=scores, y=top_topics, orientation='h', 
				 labels={'x': 'Confidence', 'y': 'Label'},
				 text=scores,
				 range_x=(0,115),
				 title='Top Topics',
				 color=np.linspace(0,1,len(scores)),
				 color_continuous_scale='GnBu')
	fig.update(layout_coloraxis_showscale=False)
	fig.update_traces(texttemplate='%{text:0.1f}%', textposition='outside')
	st.plotly_chart(fig)

def req(url):
	try:
		# For non-200 status codes
		resp = requests.get(url, headers=headers)
		resp.raise_for_status()
		soup = BeautifulSoup(resp.content, 'html.parser')
		if soup.find("div", id="comments") and soup.find("div", id="secondary"):
			remove_comments = soup.find("div", id="comments")
			remove_comments.extract()
			remove_secondary = soup.find("div", id="secondary")
			remove_secondary.extract()
			extract_text = [t.text for t in soup.find_all(['h1', 'p'])]
			paragraphs = ' '.join(extract_text)
			return paragraphs
		elif soup.find("div", id="comments") and soup.find("aside", id="secondary"):
			remove_comments = soup.find("div", id="comments")
			remove_comments.extract()
			remove_secondary = soup.find("aside", id="secondary")
			remove_secondary.extract()
			extract_text = [t.text for t in soup.find_all(['h1', 'p'])]
			paragraphs = ' '.join(extract_text)
			return paragraphs
		else:
			extract_text = [t.text for t in soup.find_all(['h1', 'p'])]
			paragraphs = ' '.join(extract_text)
			return paragraphs
	except requests.exceptions.HTTPError as err:
		st.error(err)
		st.stop()

# Main function
def main():
	with st.spinner('Classifying...'):
		try:
			global txt
			df_classify_topic = pd.DataFrame(topics_dict)
			df_classify_topic = df_classify_topic.sort_values(by='Relevance Score', ascending=False)
			top_topics = df_classify_topic['Topic'].head(10).to_list()
			scores = df_classify_topic['Relevance Score'].head(10).to_list()
		except:
			st.warning("Sorry about this, there seemed to be an error. Trying again...")
	try:
		plot_result(top_topics[::-1][-10:], scores[::-1][-10:])
	except ValueError:
		st.subheader("No topics found!")
		st.warning("""
			It looks like no topics were found for this text. This might be because the text length
   			is insufficient	or it doesn't have enough extractable terms.
      
      			Try again with longer text.
	 	""")

# Dictionaries

ent_dict = {
	'Entity': [],
	'Page URL': [],
	'Wikidata URI': [],
	'Relevance Score': []
}

topics_dict = {
	'Topic': [],
	'Page URL': [],
	'Relevance Score': []
}

categories_dict = {
	'Category': [],
	'Relevance Score': []
}

categories_multi_dict = {
	'Category': [],
	'Page URL': [],
	'Relevance Score': []
}

all_txt = []

# Streamlit stuff

st.sidebar.title('Input type selector')

input_type = st.sidebar.radio('Select your input type', ['Text', 'URL', 'Multiple URLs'])

# Determines input types
st.title('Welcome to RALTS Lite!')
st.write('This script uses natural language classification to extract entities, topics, and categories from any body of text or URL(s).')
st.info(f'Requests used today: {int(account_manager.get_account().requests_used_today)}/500')
if input_type == 'Text':
	global txt
	txt = st.text_area('Enter text to be analysed...')
	txt = txt.replace('\n', ' ').replace('"', '').replace('“','').replace('”', '').replace('‘','').replace('’', '').replace("'s", '').replace(",", '')
	st.write(len(txt))
elif input_type == 'URL':
	url = st.text_input('Enter URL')
elif input_type == 'Multiple URLs':
	multi_url = st.text_area('Enter keywords, 1 per line')

submit = st.button('Submit')

# Keyword extraction function to analyse with TextRazor

def textrazor_extraction(input_type):

	if input_type == 'Text':
		global txt
		response = client.analyze(txt)
		for entity in response.entities():
			if entity.relevance_score > 0:
				ent_dict['Entity'].append(entity.id)
				ent_dict['Page URL'].append("N/A")
				ent_dict['Wikidata URI'].append(f'https://www.wikidata.org/wiki/{entity.wikidata_id}')
				ent_dict['Relevance Score'].append(entity.relevance_score)
		
		for topic in response.topics():
			if topic.score > 0.6:
				topics_dict['Topic'].append(topic.label)
				topics_dict['Page URL'].append("N/A")
				topics_dict['Relevance Score'].append(topic.score)
		
		for category in response.categories():
			categories_dict['Category'].append(category.label)
			categories_dict['Relevance Score'].append(category.score)

	elif input_type == 'URL':
		txt = req(url)
		response = client.analyze(txt)
		for entity in response.entities():
			if entity.relevance_score > 0:
				ent_dict['Entity'].append(entity.id)
				ent_dict['Page URL'].append(url)
				ent_dict['Wikidata URI'].append(f'https://www.wikidata.org/wiki/{entity.wikidata_id}')
				ent_dict['Relevance Score'].append(entity.relevance_score)
		
		for topic in response.topics():
			if topic.score > 0.6:
				topics_dict['Topic'].append(topic.label)
				topics_dict['Page URL'].append(url)
				topics_dict['Relevance Score'].append(topic.score)
		
		for category in response.categories():
			categories_dict['Category'].append(category.label)
			categories_dict['Relevance Score'].append(category.score)

	elif input_type == 'Multiple URLs':

		for u in urls:
			try:
				txt = req(u)
				all_txt.append(txt)
				response = client.analyze(txt)
				for entity in response.entities():
					if entity.relevance_score > 0:
						ent_dict['Entity'].append(entity.id)
						ent_dict['Page URL'].append(u)
						ent_dict['Wikidata URI'].append(f'https://www.wikidata.org/wiki/{entity.wikidata_id}')
						ent_dict['Relevance Score'].append(entity.relevance_score)
				
				for topic in response.topics():
					if topic.score > 0.6:
						topics_dict['Topic'].append(topic.label)
						topics_dict['Page URL'].append(u)
						topics_dict['Relevance Score'].append(topic.score)
				
				for category in response.categories():
					categories_multi_dict['Category'].append(category.label)
					categories_multi_dict['Page URL'].append(u)
					categories_multi_dict['Relevance Score'].append(category.score)

			except Exception as e:
				st.error(e)
				continue

# DataFrames to present above data
def data_viz():

	if input_type == 'Text':

		df_ent = pd.DataFrame(ent_dict)
		df_ent = df_ent.drop(columns=['Page URL'])
		grouped_df_ent = df_ent.groupby(['Entity']).agg({'Relevance Score': ['mean'], 'Wikidata URI': ['max']}).round(3)
		grouped_df_ent = grouped_df_ent.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_ent.columns = grouped_df_ent.columns.droplevel(1)
		st.header('Entities')
		st.dataframe(grouped_df_ent)

		df_topic = pd.DataFrame(topics_dict)
		df_topic = df_topic.drop(columns=['Page URL'])
		grouped_df_topic = df_topic.groupby(['Topic']).agg({'Relevance Score': ['mean']}).round(3)
		grouped_df_topic = grouped_df_topic.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_topic.columns = grouped_df_topic.columns.droplevel(1)
		st.header('Topics')
		st.dataframe(grouped_df_topic)

		df_cat = pd.DataFrame(categories_dict)
		grouped_df_cat = df_cat.groupby(['Category']).agg({'Relevance Score': ['mean']}).round(3)
		grouped_df_cat = grouped_df_cat.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_cat.columns = grouped_df_cat.columns.droplevel(1)
		st.header('Categories')
		st.dataframe(grouped_df_cat)

	elif input_type == 'URL':

		df_ent = pd.DataFrame(ent_dict)
		grouped_df_ent = df_ent.groupby(['Entity']).agg({'Relevance Score': ['mean'], 'Wikidata URI': ['max']}).round(3)
		grouped_df_ent = grouped_df_ent.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_ent.columns = grouped_df_ent.columns.droplevel(1)
		st.header('Entities')
		st.dataframe(grouped_df_ent)

		df_topic = pd.DataFrame(topics_dict)
		grouped_df_topic = df_topic.groupby(['Topic']).agg({'Relevance Score': ['mean']}).round(3)
		grouped_df_topic = grouped_df_topic.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_topic.columns = grouped_df_topic.columns.droplevel(1)
		st.header('Topics')
		st.dataframe(grouped_df_topic)

		df_cat = pd.DataFrame(categories_dict)
		grouped_df_cat = df_cat.groupby(['Category']).agg({'Relevance Score': ['mean']}).round(3)
		grouped_df_cat = grouped_df_cat.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_cat.columns = grouped_df_cat.columns.droplevel(1)
		st.header('Categories')
		st.dataframe(grouped_df_cat)

	elif input_type == 'Multiple URLs':
		df_ent = pd.DataFrame(ent_dict)
		grouped_df_ent = df_ent.groupby(['Entity', 'Page URL']).agg({'Relevance Score': ['mean'], 'Wikidata URI': ['max']}).round(3)
		grouped_df_ent = grouped_df_ent.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_ent.columns = grouped_df_ent.columns.droplevel(1)
		st.header('Entities')
		st.dataframe(grouped_df_ent)

		df_topic = pd.DataFrame(topics_dict)
		grouped_df_topic = (
	            df_topic.groupby(["Topic", "Page URL"])
	            .agg({"Relevance Score": ["mean"]})
	            .round(3)
	        )
		grouped_df_topic = grouped_df_topic.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_topic.columns = grouped_df_topic.columns.droplevel(1)
		st.header('Topics')
		st.dataframe(grouped_df_topic)

		df_cat = pd.DataFrame(categories_multi_dict)
		grouped_df_cat = df_cat.groupby(['Category', 'Page URL']).agg({'Relevance Score': ['mean']}).round(3)
		grouped_df_cat = grouped_df_cat.reset_index().sort_values(by=('Relevance Score', 'mean'), ascending=False)
		grouped_df_cat.columns = grouped_df_cat.columns.droplevel(1)
		st.header('Categories')
		st.dataframe(grouped_df_cat)
		
# Execute functions
if submit and input_type == 'Text':
	textrazor_extraction('Text')
	data_viz()
	main()
elif submit and input_type == 'URL':
	textrazor_extraction('URL')
	data_viz()
	main()
elif submit and input_type == 'Multiple URLs':
	urls = [line for line in multi_url.split("\n")]
	textrazor_extraction('Multiple URLs')
	data_viz()
