import streamlit as st
import os
from dotenv import load_dotenv
import time

final_arr=[]
load_dotenv()


if "info" not in st.session_state:
    st.session_state.info = None
#################################################################################
# App elements

st.set_page_config(layout="wide")
st.title("Azure AI Video Demos")




text = '''

Supported scenarios & APIs:
- :speech_balloon: [Offline Subtitles](./Subtitles) generated offline subtitles
- :frame_with_picture: [Video Analytics](./Video_Analysis) video analytics dashboard
'''

st.markdown(text)