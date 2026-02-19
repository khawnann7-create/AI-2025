import streamlit as st
import random
import pandas as pd
from textblob import TextBlob

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Music will never die", layout="wide")

# ------------------ PASTEL CSS ------------------
st.markdown("""
<style>
body {
    background-color: #fff6fb;
}
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #ff6fa5;
    margin-bottom: 10px;
}
.card {
    background-color: #ffe4f0;
    padding: 15px;
    border-radius: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    text-align: center;
}
.mood-box {
    background-color: #e0f7fa;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}
.stButton>button {
    background-color: #ffb6d9;
    color: black;
    border-radius: 15px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎵 Music will never die</div>", unsafe_allow_html=True)

# ------------------ SONG DATA ------------------

songs = {
    "อินเลิฟ,มีความรัก": [
        {
            "title": "Perfect - Ed Sheeran",
            "youtube": "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
            "cover": "https://i.ytimg.com/vi/2Vv-BfVoq4g/maxresdefault.jpg"
        },
        {
            "title": "Lover - Taylor Swift",
            "youtube": "https://www.youtube.com/watch?v=-BjZmE2gtdo",
            "cover": "https://i.ytimg.com/vi/-BjZmE2gtdo/maxresdefault.jpg"
        }
    ],
    "เหนื่อย,ท้อ": [
        {
            "title": "Fix You - Coldplay",
            "youtube": "https://www.youtube.com/watch?v=k4V3Mo61fJM",
            "cover": "https://i.ytimg.com/vi/k4V3Mo61fJM/maxresdefault.jpg"
        }
    ],
    "ง่วง,เบื่อ": [
        {
            "title": "Sunflower - Post Malone",
            "youtube": "https://www.youtube.com/watch?v=ApXoWvfEYVU",
            "cover": "https://i.ytimg.com/vi/ApXoWvfEYVU/maxresdefault.jpg"
        }
    ],
    "อกหัก,เศร้า": [
        {
            "title": "Someone Like You - Adele",
            "youtube": "https://www.youtube.com/watch?v=hLQl3WQQoQ0",
            "cover": "https://i.ytimg.com/vi/hLQl3WQQoQ0/maxresdefault.jpg"
        }
    ]
}

# ------------------ SESSION STATE ------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ MOOD SELECT ------------------
st.markdown("<div class='mood-box'>เลือกความรู้สึกของคุณ 💭</div>", unsafe_allow_html=True)

mood = st.selectbox(
    "เลือกอารมณ์",
    ["อินเลิฟ,มีความรัก", "เหนื่อย,ท้อ", "ง่วง,เบื่อ", "อกหัก,เศร้า"]
)

if st.button("🎲 สุ่มเพลง"):
    song = random.choice(songs[mood])
    st.session_state.history.append(mood)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.image(song["cover"])
        st.markdown(f"### 🎵 {song['title']}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.video(song["youtube"])

# ------------------ AI ANALYZE ------------------
st.markdown("## 🤖 ให้ AI วิเคราะห์อารมณ์จากข้อความ")

user_text = st.text_input("พิมพ์ความรู้สึกของคุณ...")

if user_text:
    blob = TextBlob(user_text)
    polarity = blob.sentiment.polarity

    if polarity > 0.3:
        result = "อินเลิฟ,มีความรัก 💖"
    elif polarity < -0.3:
        result = "อกหัก,เศร้า 💔"
    elif -0.3 <= polarity <= 0.3:
        result = "ง่วง,เบื่อ 😴"
    else:
        result = "เหนื่อย,ท้อ 🥲"

    st.success(f"AI วิเคราะห์ว่า: {result}")
    st.session_state.history.append(result)

# ------------------ STATISTICS ------------------
st.markdown("## 📊 สถิติอารมณ์ผู้ใช้")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history, columns=["Mood"])
    st.bar_chart(df["Mood"].value_counts())
else:
    st.info("ยังไม่มีข้อมูลสถิติ")
