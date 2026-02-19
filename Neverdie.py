import streamlit as st
import pandas as pd
from textblob import TextBlob

st.set_page_config(page_title="Music will never die", layout="wide")

# ------------------ CSS PASTEL ------------------
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
    margin-bottom: 20px;
}
.carousel {
    display: flex;
    overflow-x: auto;
    gap: 20px;
    padding: 20px 0;
}
.card {
    min-width: 220px;
    background: #ffe4f0;
    padding: 10px;
    border-radius: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    text-align: center;
}
.card img {
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎵 Music will never die</div>", unsafe_allow_html=True)

# ------------------ SONG DATA ------------------

songs = {
    "อินเลิฟ,มีความรัก": [
        {"title": "Perfect - Ed Sheeran",
         "youtube": "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
         "cover": "https://i.ytimg.com/vi/2Vv-BfVoq4g/maxresdefault.jpg"},
        {"title": "Lover - Taylor Swift",
         "youtube": "https://www.youtube.com/watch?v=-BjZmE2gtdo",
         "cover": "https://i.ytimg.com/vi/-BjZmE2gtdo/maxresdefault.jpg"},
        {"title": "All of Me - John Legend",
         "youtube": "https://www.youtube.com/watch?v=450p7goxZqg",
         "cover": "https://i.ytimg.com/vi/450p7goxZqg/maxresdefault.jpg"}
    ],
    "เหนื่อย,ท้อ": [
        {"title": "Fix You - Coldplay",
         "youtube": "https://www.youtube.com/watch?v=k4V3Mo61fJM",
         "cover": "https://i.ytimg.com/vi/k4V3Mo61fJM/maxresdefault.jpg"},
        {"title": "Let It Be - The Beatles",
         "youtube": "https://www.youtube.com/watch?v=QDYfEBY9NM4",
         "cover": "https://i.ytimg.com/vi/QDYfEBY9NM4/maxresdefault.jpg"}
    ],
    "ง่วง,เบื่อ": [
        {"title": "Sunflower - Post Malone",
         "youtube": "https://www.youtube.com/watch?v=ApXoWvfEYVU",
         "cover": "https://i.ytimg.com/vi/ApXoWvfEYVU/maxresdefault.jpg"},
        {"title": "Stay - The Kid LAROI",
         "youtube": "https://www.youtube.com/watch?v=kTJczUoc26U",
         "cover": "https://i.ytimg.com/vi/kTJczUoc26U/maxresdefault.jpg"}
    ],
    "อกหัก,เศร้า": [
        {"title": "Someone Like You - Adele",
         "youtube": "https://www.youtube.com/watch?v=hLQl3WQQoQ0",
         "cover": "https://i.ytimg.com/vi/hLQl3WQQoQ0/maxresdefault.jpg"},
        {"title": "Happier Than Ever - Billie Eilish",
         "youtube": "https://www.youtube.com/watch?v=5GJWxDKyk3A",
         "cover": "https://i.ytimg.com/vi/5GJWxDKyk3A/maxresdefault.jpg"}
    ]
}

# ------------------ SESSION ------------------
if "selected_song" not in st.session_state:
    st.session_state.selected_song = None

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ SELECT MOOD ------------------

mood = st.selectbox(
    "💭 เลือกความรู้สึกของคุณ",
    ["อินเลิฟ,มีความรัก", "เหนื่อย,ท้อ", "ง่วง,เบื่อ", "อกหัก,เศร้า"]
)

st.markdown("### 🎬 เลือกเพลงที่คุณชอบ")

# ------------------ CAROUSEL ------------------

cols = st.columns(len(songs[mood]))

for i, song in enumerate(songs[mood]):
    with cols[i]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if st.button("▶ เลือก", key=song["title"]):
            st.session_state.selected_song = song
            st.session_state.history.append(mood)

        st.image(song["cover"])
        st.markdown(f"**{song['title']}**")
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------ VIDEO PLAYER ------------------

if st.session_state.selected_song:
    st.markdown("## 🎵 Now Playing")
    st.video(st.session_state.selected_song["youtube"])

# ------------------ AI ANALYZE ------------------

st.markdown("## 🤖 วิเคราะห์อารมณ์จากข้อความ")

user_text = st.text_input("พิมพ์ความรู้สึกของคุณ...")

if user_text:
    blob = TextBlob(user_text)
    polarity = blob.sentiment.polarity

    if polarity > 0.3:
        result = "อินเลิฟ,มีความรัก"
    elif polarity < -0.3:
        result = "อกหัก,เศร้า"
    elif -0.3 <= polarity <= 0.3:
        result = "ง่วง,เบื่อ"
    else:
        result = "เหนื่อย,ท้อ"

    st.success(f"AI วิเคราะห์ว่า: {result}")
    st.session_state.history.append(result)

# ------------------ STATS ------------------

st.markdown("## 📊 สถิติอารมณ์ผู้ใช้")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history, columns=["Mood"])
    st.bar_chart(df["Mood"].value_counts())
else:
    st.info("ยังไม่มีข้อมูล")
