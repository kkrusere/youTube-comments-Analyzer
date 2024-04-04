import os, sys

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime

import googleapiclient.discovery

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config( page_title="YouTube Comment Analyzer",
                    page_icon= "random",
                    layout="wide"
 )

import platform

# Get Python version
python_version = platform.python_version()

# Print Python version on Streamlit
st.write(f"Python Version: {python_version}")

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


st.markdown("----")




col1, col2, col3 = st.columns((.1,1,.1))

with col1:
    st.write("")

with col2:
    # Input field for video URL
    video_url = st.text_input("Enter YouTube Video URL:", key="video_url_input")

with col3:
    st.write("")


st.markdown("----")

video = None
title = None
thumbnail_url = None
view_count = None
like_count = None
date_posted = None
youtube = None
description = None

###############################################################################################
######### Have a video URL
if video_url:
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
    thumbnail_url = video["snippet"]["thumbnails"]["default"]["url"]
    view_count = video["statistics"]["viewCount"]
    like_count = video["statistics"]["likeCount"]
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

#######################################################**************getting some comments**************##################################################
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)


##########################################################   

data = []

try:
    wait = WebDriverWait(driver, 1)

    # Open the YouTube video
    driver.get("https://www.youtube.com/watch?v=O9SGkC5UDE4")

    # Scroll down to load comments
    for item in range(200):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(1)

    # Get all comments
    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
        data.append(comment.text)

finally:
    # Close the WebDriver session
    driver.quit() 

st.write(len(data))
st.write(data[:5])

###########################################################################################################################################################
st.markdown("----")

## Have a Topic
# Define the search term
search_term = st.text_input("Enter Topic:", key="Electric Vehicles")

if search_term:
    # Search for videos
    response = youtube.search().list(
        q=search_term,
        type="video",
        part="id,snippet",
        maxResults=10
    ).execute()

    # Extract video IDs and titles
    video_ids = []
    video_titles = []
    for video in response["items"]:
        video_ids.append(video["id"]["videoId"])
        video_titles.append(video["snippet"]["title"])


    col1, col2, col3= st.columns((1,.1,1))

    with col1:
        # Print the first 5 video titles and URLs
        for i, title in enumerate(video_titles[:5], start=1):
            st.write(f"{i}. {title}")
            st.write(f"URL: https://www.youtube.com/watch?v={video_ids[i-1]}")
    with col2:
        pass
    with col3:
        # Print the last half of video titles and URLs
        for i, title in enumerate(video_titles[len(video_titles)//2:], start=6):
            st.write(f"{i}. {title}")
            st.write(f"URL: https://www.youtube.com/watch?v={video_ids[len(video_titles)//2 + i - 6]}")
