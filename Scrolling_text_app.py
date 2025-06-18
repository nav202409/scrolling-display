import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Scrolling Display",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit UI and set up layout
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding: 0rem !important;}

    .scroll-container {
        width: 100vw;
        height: 100vh;
        background-color: black;
        display: flex;
        align-items: center;
        overflow: hidden;
    }

    .scroll-text {
        font-size: 14vw;
        font-weight: bold;
        color: white;
        white-space: nowrap;
        display: inline-block;
        padding-left: 100%;
        animation: scroll-left 20s linear infinite;
    }

    @keyframes scroll-left {
        0%   { transform: translateX(0%); }
        100% { transform: translateX(-100%); }
    }
    </style>
""", unsafe_allow_html=True)

# Convert Google Sheet to CSV link
sheet_url = st.secrets["sheet_url"]

# Fix export path from Google Sheet
match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url)
gid_match = re.search(r"[#?]gid=([0-9]+)", sheet_url)

if match and gid_match:
    file_id = match.group(1)
    gid = gid_match.group(1)
    csv_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid={gid}"
else:
    st.error("Invalid Google Sheet URL")

# Read messages from first column
df = pd.read_csv(csv_url, header=None)
messages = df[0].dropna().tolist()
combined_message = "  ⏺  ".join(messages)

# Render scrolling text
st.markdown(f"""
<div class="scroll-container">
    <div class="scroll-text">{combined_message}</div>
</div>
""", unsafe_allow_html=True)
