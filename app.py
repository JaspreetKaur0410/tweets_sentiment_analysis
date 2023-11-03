import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets")
st.sidebar.title("Tweets Analysis")

st.markdown("This application is built to analyze the sentiments of Tweets 🐦")
st.sidebar.markdown("This application is built to analyze the sentiments of Tweets 🐦")

BASE_DIR = os.getcwd()
print(BASE_DIR)
csv_path = "data/Tweets.csv"
#cache the output of function if input doesn't change - cached output will be stored/persisted on disk
# @st.cache_data(persist=True)
def load_data():
    data=pd.read_csv(os.path.join(BASE_DIR, csv_path))
    data["tweet_created"]=pd.to_datetime(data["tweet_created"])
    return data

data=load_data()

st.sidebar.subheader("Show random Tweet")
random_tweet=st.sidebar.radio('Sentiment',('positive','negative','neutral'))
st.sidebar.info((data.query('airline_sentiment==@random_tweet'))[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown(" ### Number of tweets by Sentiment")
select=st.sidebar.selectbox('Visualization Type', ['Histogram','PieChart'],key='1')
sentiment_count=data['airline_sentiment'].value_counts()
sentiment_count=pd.DataFrame({'Sentiment':sentiment_count.index,'Tweets':sentiment_count.values})

if  not st.sidebar.checkbox("Hide",False):
    st.markdown("### Number of Tweets by Sentiments")
    if select=="Histogram":
        fig=px.bar(sentiment_count,x="Sentiment",y="Tweets",color='Tweets',height=500)
        st.plotly_chart(fig)
    else:
        fig=px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(fig)
        
st.sidebar.subheader("When and Where are users Tweeting from?")
hour=st.sidebar.slider("Hour of Day",0,23)
data_acc_to_hour=(data[data['tweet_created'].dt.hour==hour]).dropna()
if not st.sidebar.checkbox("Close", False, key='2'):
    st.markdown("### Tweets location based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00" %(len(data_acc_to_hour), hour, (hour+1)%24))
    st.map(data_acc_to_hour)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(data_acc_to_hour)
        
st.sidebar.subheader("Airline Tweets By Sentiments")
choice=st.sidebar.multiselect('Pick airlines',(data['airline']).unique(),key='3')

if len(choice)>0:
    choice_data=data[data.airline.isin(choice)]
    # st.write(choice_data)
    fig_choice=px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
                            facet_col='airline_sentiment', height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment=st.sidebar.radio('Choose sentiment to Display Word Cloud!', ('positive','negative','neutral'))

if not st.sidebar.checkbox("Close",False,key='4'):
    st.header("Word Cloud for %s" % (word_sentiment))
    data_acc_to_sentiment=data[data['airline_sentiment']==word_sentiment]
    words=' '.join(data_acc_to_sentiment['text'])
    process_words=' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word!='RT'])
    wordcloud=WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(process_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
