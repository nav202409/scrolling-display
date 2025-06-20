import streamlit as st
import pandas as pd
import re

st.set_page_config(layout="centered", page_title="Scrolling Messages", page_icon="📰")

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

# Compatibility-optimized CSS for scrolling
scroll_css = """
<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  background-color: black;
  overflow: hidden;
  position: relative;
}

/* For iOS 11-15 compatibility */
body {
  padding: constant(safe-area-inset);
  padding: env(safe-area-inset);
  background-color: black;
}

/* Remove extra spacing around content */
.block-container {
  padding: 0rem !important;
  margin: 0rem !important;
}

/* Hide Streamlit UI elements */
#MainMenu, header, footer {
  visibility: hidden;
}

/* Scrolling container with simplified layout */
.scroll-container {
  width: 100vw;
  height: 100vh;
  background-color: black;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  overflow: hidden;
  position: absolute;
  inset: 0;
}

/* Scrolling text with smaller font for older devices */
.scroll-text {
  font-size: 6vw;
  font-weight: bold;
  color: white;
  white-space: nowrap;
  display: inline-block;
  padding-left: 100%;
  animation: scroll-left 30s linear infinite;
}

/* Keyframe animation */
@keyframes scroll-left {
  0%   { transform: translateX(0%); }
  100% { transform: translateX(-100%); }
}
</style>
"""

# Render HTML and CSS
st.markdown(scroll_css, unsafe_allow_html=True)
st.markdown(f"""
<div class="scroll-container">
  <div class="scroll-text">{combined_message}</div>
</div>
""", unsafe_allow_html=True)
