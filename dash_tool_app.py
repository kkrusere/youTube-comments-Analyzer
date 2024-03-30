import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

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


