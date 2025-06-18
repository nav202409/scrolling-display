import streamlit as st
import pandas as pd
import re

st.set_page_config(layout="centered", page_title="Scrolling Messages", page_icon="📰")

# Auto-refresh every 60 seconds
st.markdown("""
    <meta http-equiv="refresh" content="60">
""", unsafe_allow_html=True)

# Read and parse Google Sheet URL from secrets
sheet_url = st.secrets["sheet_url"]

# Convert to CSV export URL
match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url)
gid_match = re.search(r"[#?]gid=([0-9]+)", sheet_url)

if match and gid_match:
    file_id = match.group(1)
    gid = gid_match.group(1)
    csv_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid={gid}"
else:
    st.error("Invalid Google Sheet URL")

# Load messages from column A
df = pd.read_csv(csv_url, header=None)
messages = df[0].dropna().tolist()

# Combine messages into one
combined_message = "  •  ".join(messages)

# CSS for scrolling

scroll_css = """
<style>
/* Full black background across all areas, including safe insets */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  background-color: black;
  overflow: hidden;
  -webkit-overflow-scrolling: touch;
  position: fixed;
  inset: 0;
}

/* Streamlit UI elements hidden */
#MainMenu, header, footer {
  visibility: hidden;
}

/* Remove extra padding */
.block-container {
  padding: 0rem !important;
  margin: 0rem !important;
}

/* Use safe area fill (for iPhones with notch etc) */
body {
  padding: env(safe-area-inset);
  background-color: black;
}

/* Scrolling container */
.scroll-container {
  width: 100vw;
  height: 100vh;
  background-color: black;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  overflow: hidden;
  position: fixed;
  inset: 0;
}

/* The scrolling message itself */
.scroll-text {
  font-size: 10vw;
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
"""


# Render
st.markdown(scroll_css, unsafe_allow_html=True)
st.markdown(f"""
<div class="scroll-container">
  <div class="scroll-text">{combined_message}</div>
</div>
""", unsafe_allow_html=True)
