import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
import time

load_dotenv(find_dotenv())

if "info" not in st.session_state:
    st.session_state.info = None

st.set_page_config(layout="wide")
st.title("Video Subtitles")

# fetch subtitles from "subtitles" folder
subtitles = os.listdir("subtitles")
selected_subtitle = st.selectbox("Select a subtitle file", subtitles)

# read the selected subtitle file
with open(f"subtitles/{selected_subtitle}") as f:
    subtitle = f.read()

st.write(f"## Selected subtitle file: {selected_subtitle}")

st.video("https://mmadatalake.blob.core.windows.net/tmp-shr/95388K11-short.mp4?sv=2023-11-03&st=2024-05-22T20%3A44%3A37Z&se=2025-05-23T20%3A44%3A00Z&sr=b&sp=r&sig=RGBppmQfMcNjxqA4KpyD8TehyWK5stb9NnKydcmbqKA%3D", subtitles=subtitle, autoplay=True)