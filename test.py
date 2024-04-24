
from streamlit_option_menu import option_menu
import streamlit as st
# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go

# import matplotlib.pyplot as plt
# from wordcloud import WordCloud

import googleapiclient.discovery


# YouTube API key
api_key = st.secrets["YouTubeAPI_key"]

# Create YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)


st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config( page_title="YouTube Comment Analyzer",
                    page_icon= "random",
                    layout="wide"
 )

import platform

# import json
# from bs4 import BeautifulSoup
# import pandas as pd
# import datetime 
# import random
# # Import date class from datetime module
# from datetime import date

import datetime
#import config

# import pickle as pkle
# import os.path

from streamlit_server_state import server_state, server_state_lock

# import requests
import streamlit.components.v1 as components

import platform

# Get Python version
python_version = platform.python_version()

# Print Python version on Streamlit
st.write(f"Python Version: {python_version}")

with st.sidebar:
    choose = option_menu("Dash Menu", ["About the Project", "Video Summary Stats", "Topic Search", "Sentiment Analysis", "WordCloud"],
                         icons=['','', '','', ''],
                         menu_icon="youtube", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#636EFA"},
    }
    )



if choose == "About the Project":
#Add the cover image for the cover page. Used a little trick to center the image
    col1, col2, col3 = st.columns((.1,1,.1))

    with col1:
        st.write("")

    with col2:
        st.markdown(" <h1 style='text-align: center;'>YouTube Comment Analyser</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><i><b> YouTube-comments-Analyzer is a tool to analyze audience sentiment, "
                "perspective, topics, and engagement of YouTube video comments. It collects and preprocesses comments, performs "
                "sentiment analysis and topic modeling, and visualizes findings through an interactive dashboard. Beneficial for "
                "content creators, marketers, and researchers. </b></i></p>", unsafe_allow_html=True)
        st.markdown("<center><img src='https://github.com/kkrusere/Market-Basket-Analysis-on-the-Online-Retail-Data/blob/main/Assets/comments_analyzer.jpg?raw=1' width=300/></center>", unsafe_allow_html=True)

    with col3:
        st.write("")

    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown("#### **About the Project:**")

        st.markdown("""
                
                ##### **Abstract**

                
        """)

        st.markdown("##### ***Project Contributors:***")
        st.markdown("Kuzi Rusere")
        

elif choose == "Video Summary Stats":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: black;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Video Summary Stats</p>', unsafe_allow_html=True)
    keywords = ["Sentiment-Analysis"] # this is going to be our keyword 

    
    st.markdown("---")
    ######################################################################
    col1, col2, col3 = st.columns((.1,1,.1))

    with col1:
        st.write("")

    with col2:
        # Input field for video URL
        video_url = st.text_input("Enter YouTube Video URL:", key="video_url_input")

    with col3:
        st.write("")

    st.markdown("---")
    ######################################################################

    video = None
    title = None
    thumbnail_url = None
    view_count = None
    like_count = None
    date_posted = None
    youtube = None
    description = None
    response = None

    
    ######### Have a video URL
    if video_url != "":
        # Extract video ID from URL
        video_id = video_url.split('=', 1)[-1]

        # YouTube API key
        api_key = st.secrets["YouTubeAPI_key"]

        # Create YouTube API client
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
   
        # Request video details
        response = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()
#############################################################################################
    

        # Extract required information
        video = response["items"][0]
        title = video["snippet"]["title"]
        thumbnail_url = video["snippet"]["thumbnails"]["maxres"]["url"]
        view_count = video["statistics"]["viewCount"]
        like_count = video["statistics"]["likeCount"]
        commentCount = video["statistics"]["commentCount"]
        date_posted = video["snippet"]["publishedAt"]
        description = video["snippet"]["description"]


   ####################
        col1, col2, col3= st.columns((1,.1,1))
        with col1:
            if video_url:
                # Display video details
                st.title(title)

                date_object = datetime.datetime.strptime(date_posted, "%Y-%m-%dT%H:%M:%SZ")
                # Format the date object
                date_formatted = date_object.strftime("%Y-%m-%d %H:%M:%S")

                st.write(f"Date posted: {date_formatted}")
                # Split the description by newlines
                paragraphs = description.split("\n")
                # Get the first paragraph
                first_paragraph = paragraphs[0]

                st.write(f"Description: {first_paragraph}")
                
        with col2:
            pass

        with col3:
            if video_url:
                st.markdown(F"<center><img src={thumbnail_url} width=300/></center>", unsafe_allow_html=True)

                st.write(f"View count: {view_count}")
                st.write(f"Like count: {like_count}")



#######################################################*******************************************************####################################################################

elif choose == "Topic Search":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: black;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Topic Search</p>', unsafe_allow_html=True)

    st.markdown("---")
    ######################################################################

    def get_video_info(video_id):
        # Request video details
        response = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()

        # Extract required information
        video = response["items"][0]
        title = video["snippet"]["title"]
        view_count = video["statistics"]["viewCount"]
        like_count = video["statistics"]["likeCount"]
        commentCount = video["statistics"]["commentCount"]
        date_posted = video["snippet"]["publishedAt"]
        description = video["snippet"]["description"]


        date_str = date_posted
        date_object = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

        # Format the date object
        date_posted = date_object.strftime("%Y-%m-%d %H:%M:%S")


        # Split the description by newlines
        paragraphs = description.split("\n")

        # Get the first paragraph
        first_paragraph = paragraphs[0]

        extracted_video_url = f"https://www.youtube.com/watch?v={video_id}"


        # Print the information
        st.write("Title:", title)
        st.write("Video URL:", extracted_video_url)
        st.write("View count:", view_count)
        st.write("Like count:", like_count)
        st.write("Number of Comments:", commentCount)
        st.write("Date posted:", date_posted)
        st.write("Description:", first_paragraph)
        st.write("\n\n\n")

    # Search for videos using the YouTube API
    def search_videos(query, youtube = youtube):

        # Request video search
        response = youtube.search().list(
            q=query,
            type="video",
            part="id,snippet",
            maxResults=10
        ).execute()

        # Extract video IDs from search results
        video_ids = []
        for item in response["items"]:
            video_ids.append(item["id"]["videoId"])

        return video_ids


    def input_topic_for_search():
        topic_placeholder = st.empty()  # Placeholder for topic input

        # Get name input
        topic = topic_placeholder.text_input("Enter your Topic:")


        # Clear the placeholders 
        if topic:
            topic_placeholder.empty()
     


    topic_for_search = input_topic_for_search()

    video_ids = search_videos(topic_for_search)


    for video_id in video_ids:
        get_video_info(video_id)


############################################################*******************************************########################################################

elif choose == "Sentiment Analysis":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: black;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Sentiment Analysis</p>', unsafe_allow_html=True)

    st.markdown("---")
    ######################################################################

    with st.echo():
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.os_manager import ChromeType

        @st.cache_resource
        def get_driver():
            return webdriver.Chrome(
                service=Service(
                    ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                ),
                options=options,
            )

        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")

        driver = get_driver()
        driver.get("http://example.com")

        st.code(driver.page_source)
    
#######################################################*******************************************###############################################################


elif choose == "WordCloud":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: black;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">WordCloud</p>', unsafe_allow_html=True)

    st.markdown("---")
    ######################################################################