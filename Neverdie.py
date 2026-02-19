import streamlit as st
import pandas as pd

st.set_page_config(page_title="Music will never die", layout="wide")

# -------------------- PASTEL UI --------------------
st.markdown("""
<style>
body {
    background-color: #fff6fb;
}

.title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    color: #ff6fa5;
    margin-bottom: 30px;
}

.card {
    background: #ffe4f0;
    padding: 12px;
    border-radius: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
    text-align: center;
}

.card img {
    border-radius: 15px;
    width: 100%;
}

.mood-box {
    background: #e0f7fa;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎵 Music will never die</div>", unsafe_allow_html=True)

# -------------------- เพลงไทย --------------------

songs = {
    "อินเลิฟ,มีความรัก": [
        {"title": "คลั่งรัก - First Anuwat",
         "youtube": "https://www.youtube.com/watch?v=8sYkCwE0ZcI",
         "cover": "https://i.ytimg.com/vi/8sYkCwE0ZcI/maxresdefault.jpg"},
        {"title": "คนโปรด - Billkin",
         "youtube": "https://www.youtube.com/watch?v=dYIT_1iKp8Y",
         "cover": "https://i.ytimg.com/vi/dYIT_1iKp8Y/maxresdefault.jpg"},
        {"title": "แพ้ทาง - LABANOON",
         "youtube": "https://www.youtube.com/watch?v=VvZ1JxFqZ9Y",
         "cover": "https://i.ytimg.com/vi/VvZ1JxFqZ9Y/maxresdefault.jpg"}
    ],
    "เหนื่อย,ท้อ": [
        {"title": "กำลังใจ - โฮป",
         "youtube": "https://www.youtube.com/watch?v=H-4gC4JbGzY",
         "cover": "https://i.ytimg.com/vi/H-4gC4JbGzY/maxresdefault.jpg"},
        {"title": "ชีวิตยังคงสวยงาม - Bodyslam",
         "youtube": "https://www.youtube.com/watch?v=9Xb6kM1l8Yk",
         "cover": "https://i.ytimg.com/vi/9Xb6kM1l8Yk/maxresdefault.jpg"}
    ],
    "ง่วง,เบื่อ": [
        {"title": "ลาลาลอย - The TOYS",
         "youtube": "https://www.youtube.com/watch?v=Vv7Ww0P0z7g",
         "cover": "https://i.ytimg.com/vi/Vv7Ww0P0z7g/maxresdefault.jpg"},
        {"title": "Vacation Time - Part Time Musicians",
         "youtube": "https://www.youtube.com/watch?v=yb5vF6XzRzE",
         "cover": "https://i.ytimg.com/vi/yb5vF6XzRzE/maxresdefault.jpg"}
    ],
    "อกหัก,เศร้า": [
        {"title": "ถ้าเราเจอกันอีก - Tilly Birds",
         "youtube": "https://www.youtube.com/watch?v=7ZkC1zR9C1g",
         "cover": "https://i.ytimg.com/vi/7ZkC1zR9C1g/maxresdefault.jpg"},
        {"title": "แพ้คำว่ารัก - Calories Blah Blah",
         "youtube": "https://www.youtube.com/watch?v=HWhm6uFzK8Y",
         "cover": "https://i.ytimg.com/vi/HWhm6uFzK8Y/maxresdefault.jpg"}
    ]
}

# -------------------- SESSION --------------------

if "selected_song" not in st.session_state:
    st.session_state.selected_song = None

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------- เลือกอารมณ์ --------------------

st.markdown("<div class='mood-box'>💭 เลือกความรู้สึกของคุณ</div>", unsafe_allow_html=True)

mood = st.selectbox(
    "เลือกอารมณ์",
    ["อินเลิฟ,มีความรัก", "เหนื่อย,ท้อ", "ง่วง,เบื่อ", "อกหัก,เศร้า"]
)

st.markdown("### 🎬 เลือกเพลงที่คุณอยากฟัง")

cols = st.columns(len(songs[mood]))

for i, song in enumerate(songs[mood]):
    with cols[i]:
        if st.button("▶ เล่น", key=song["title"]):
            st.session_state.selected_song = song
            st.session_state.history.append(mood)

        st.image(song["cover"])
        st.markdown(f"**{song['title']}**")

# -------------------- เล่นเพลง --------------------

if st.session_state.selected_song:
    st.markdown("## 🎵 Now Playing")
    st.video(st.session_state.selected_song["youtube"])

# -------------------- AI วิเคราะห์แบบง่าย --------------------

st.markdown("## 🤖 วิเคราะห์อารมณ์จากข้อความ")

def analyze_mood(text):
    text = text.lower()

    if any(word in text for word in ["รัก", "คิดถึง", "ชอบ"]):
        return "อินเลิฟ,มีความรัก"
    elif any(word in text for word in ["เหนื่อย", "ท้อ", "หมดแรง"]):
        return "เหนื่อย,ท้อ"
    elif any(word in text for word in ["ง่วง", "เบื่อ", "เซ็ง"]):
        return "ง่วง,เบื่อ"
    elif any(word in text for word in ["เศร้า", "อกหัก", "เสียใจ"]):
        return "อกหัก,เศร้า"
    else:
        return "ง่วง,เบื่อ"

user_text = st.text_input("พิมพ์ความรู้สึกของคุณ...")

if user_text:
    result = analyze_mood(user_text)
    st.success(f"AI วิเคราะห์ว่า: {result}")
    st.session_state.history.append(result)
