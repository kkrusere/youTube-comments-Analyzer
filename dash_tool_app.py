import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import googleapiclient.discovery

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config( page_title="YouTube Comment Analyzer",
                    page_icon= "random",
                    layout="wide"
 )

col1, col2, col3 = st.columns((.1,1,.1))

with col1:
    st.write("")

with col2:
    st.markdown(" <h1 style='text-align: center;'>YouTube Comment Analyser</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'><i><b> YouTube-comments-Analyzer is a tool to analyze audience sentiment, "
                "perspective, topics, and engagement of YouTube video comments. It collects and preprocesses comments, performs "
                "sentiment analysis and topic modeling, and visualizes findings through an interactive dashboard. Beneficial for "
                "content creators, marketers, and researchers. </b></i></p>", unsafe_allow_html=True)
    st.markdown("<center><img src='https://github.com/kkrusere/youTube-comments-Analyzer/blob/main/assets/comments_analyzer.jpg?raw=1' width=600/></center>", unsafe_allow_html=True)


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

if video_url:
    # Extract video ID from URL
    video_id = video_url.split('=')[-1]

    # YouTube API key
    api_key = st.secrets["YouTubeAPI_key"]

    # Create YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Request video details
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    # Extract required information
    video = response["items"][0]
    title = video["snippet"]["title"]
    thumbnail_url = video["snippet"]["thumbnails"]["default"]["url"]
    view_count = video["statistics"]["viewCount"]
    like_count = video["statistics"]["likeCount"]
    date_posted = video["snippet"]["publishedAt"]
    description = video["snippet"]["description"]

    # Display video details
    st.title(title)
    st.image(thumbnail_url, caption="Thumbnail")
    st.write(f"View count: {view_count}")
    st.write(f"Like count: {like_count}")
    st.write(f"Date posted: {date_posted}")
    st.write(f"Description: {description}")