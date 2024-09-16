import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="YouTube Comment Analyzer",
    page_icon="random",
    layout="wide"
)

# Create the sidebar menu
with st.sidebar:
    choose = option_menu("Dash Menu", ["Project Description", "Overview & Key Metrics", "Sentiment Deep Dive", "Topic Exploration", "Engagement Analysis"],
                         icons=['info', 'clipboard-data', 'bar-chart-line', 'search', 'people'],  # Changed 'house' to 'dashboard'
                         menu_icon="cast", default_index=0,  # Set default index to Project Description
                         styles={
                             "container": {"padding": "5!important", "background-color": "#fafafa"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#636EFA"},
                         }
                         )

# Create columns for layout
col1, col2, col3 = st.columns((.1, 1, .1))

# Content for "Project Description"
if choose == "Project Description":
    with col2:
        # Title and description
        st.markdown("<h1 style='text-align: center;'>YouTube Comment Analyzer</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><i><b>YouTube-comments-Analyzer is a tool to analyze audience sentiment, "
                    "perspective, topics, and engagement of YouTube video comments. It collects and preprocesses comments, performs "
                    "sentiment analysis and topic modeling, and visualizes findings through an interactive dashboard. Beneficial for "
                    "content creators, marketers, and researchers.</b></i></p>", unsafe_allow_html=True)

        # Image in the center
        st.markdown("<center><img src='https://github.com/kkrusere/Market-Basket-Analysis-on-the-Online-Retail-Data/blob/main/Assets/comments_analyzer.jpg?raw=1' width=300/></center>", unsafe_allow_html=True)

        # Horizontal line separator
        st.markdown("----")

# Input field for YouTube URL
st.sidebar.subheader("Input Video URL")
video_url = st.sidebar.text_input("Enter the YouTube video URL:")

# Check if a valid URL is provided
if video_url:
    # Simulate fetching video data (Replace with actual API calls to YouTube Data API)
    st.sidebar.success("Video URL accepted! Fetching data...")
    # Example of parsing video ID (in practice, validate and handle exceptions)
    video_id = video_url.split("v=")[-1]
    
    # Placeholder for loading video details, comments, and analysis data
    # In practice, call functions to fetch data based on `video_id`

    # Main content based on the selected menu item
    if choose == "Overview & Key Metrics":
        st.header("Overview and Key Metrics")
        
        # Sample Data (Replace with your data loading logic)
        video_details = {"Title": "Sample Video", "Views": 10000, "Likes": 800, "Dislikes": 50}
        st.subheader("Video Details")
        st.write(f"**Title:** {video_details['Title']}")
        st.write(f"**Views:** {video_details['Views']}")
        st.write(f"**Likes/Dislikes Ratio:** {video_details['Likes'] / max(1, video_details['Dislikes'])}")

        # Sentiment Distribution Pie Chart
        sentiment_data = {'Sentiment': ['Positive', 'Negative', 'Neutral'], 'Count': [120, 30, 50]}
        sentiment_df = pd.DataFrame(sentiment_data)
        fig = px.pie(sentiment_df, names='Sentiment', values='Count', title='Sentiment Distribution')
        st.plotly_chart(fig)

        # Top Topics Word Cloud
        st.subheader("Top Topics")
        text = "Python Data Science Machine Learning AI NLP Deep Learning"
        wordcloud = WordCloud(width=800, height=400).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Engagement Highlights
        st.subheader("Engagement Highlights")
        st.write("1. **Most Liked Comment:** This is an awesome video! (200 likes)")
        st.write("2. **Second Most Liked Comment:** Very informative, thanks! (150 likes)")
        st.write("3. **Most Replied Comment:** What about more details on topic X? (50 replies)")

    elif choose == "Sentiment Deep Dive":
        st.header("Sentiment Deep Dive")
        
        # Sentiment Over Time
        st.subheader("Sentiment Over Time")
        time_sentiment_data = {'Time': [1, 2, 3, 4, 5], 'Positive': [5, 15, 20, 25, 30], 'Negative': [2, 3, 4, 5, 6]}
        df = pd.DataFrame(time_sentiment_data)
        fig = px.line(df, x='Time', y=['Positive', 'Negative'], labels={'value': 'Sentiment Score', 'Time': 'Time (minutes)'}, title='Sentiment Over Time')
        st.plotly_chart(fig)

        # Sentiment by Topic
        st.subheader("Sentiment by Topic")
        topic_sentiment_data = {'Topic': ['Python', 'AI', 'NLP'], 'Positive': [70, 50, 80], 'Negative': [10, 20, 5]}
        df = pd.DataFrame(topic_sentiment_data)
        fig = px.bar(df, x='Topic', y=['Positive', 'Negative'], barmode='group', title='Sentiment by Topic')
        st.plotly_chart(fig)

    elif choose == "Topic Exploration":
        st.header("Topic Exploration")
        
        # Interactive Word Cloud
        st.subheader("Interactive Word Cloud")
        st.write("Click on words to filter comments related to them.")
        # Example static word cloud
        text = "Python AI Data Science Visualization Machine Learning Deep Learning Neural Networks"
        wordcloud = WordCloud(width=800, height=400).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Topic Trend Analysis
        st.subheader("Topic Trend Analysis")
        st.write("Tracking topic frequency over time can reveal emerging trends or shifts in audience interest.")
        # Placeholder for future advanced analysis

    elif choose == "Engagement Analysis":
        st.header("Engagement Analysis")
        
        # Engagement Heatmap
        st.subheader("Engagement Heatmap")
        st.write("Visualize comment engagement (likes, replies) over time using a heatmap.")
        # Placeholder for heatmap visualization (you can use seaborn or plotly)

        # Influential Commenters
        st.subheader("Influential Commenters")
        st.write("Identify users with highly engaged comments and their sentiment or topical focus.")
        # Placeholder for identifying influential commenters
else:
    st.sidebar.error("Please enter a valid YouTube video URL to begin analysis.")
