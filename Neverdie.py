import streamlit as st
import random
import urllib.parse
import pandas as pd

# =============================
# Page Config
# =============================
st.set_page_config(
    page_title="Music will never die",
    page_icon="🎵",
    layout="centered"
)

# =============================
# Pastel UI
# =============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #ffd6e8, #d6f6ff);
}
.title {
    font-size: 38px;
    font-weight: bold;
    text-align: center;
    color: #ff6fa5;
}
.subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 20px;
}
textarea {
    background-color: #fff0f6 !important;
    border-radius: 20px !important;
    border: 2px solid #ffc2d1 !important;
}
.stButton>button {
    background-color: #ff8fab;
    color: white;
    border-radius: 20px;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 25px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    margin-top: 20px;
    text-align: center;
}
.counter {
    font-size: 14px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎵 Music will never die</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>พิมพ์ความรู้สึก แล้วให้ดนตรีช่วยคุณ 💖</div>", unsafe_allow_html=True)

# =============================
# ฟังก์ชันสร้างเพลง
# =============================
def create_song_list(song_names):
    songs = []
    for name in song_names:
        query = urllib.parse.quote(name)
        embed = f"https://www.youtube.com/embed?listType=search&list={query}"
        link = f"https://www.youtube.com/results?search_query={query}"
        songs.append({"title": name, "embed": embed, "link": link})
    return songs

# เพลงจริง (10 เพลง x5 = 50)
love_songs = create_song_list([
    "NONT TANONT - โต๊ะริม",
    "Billkin - โคตรพิเศษ",
    "Bowkylion - วิงวอน",
    "Three Man Down - ถ้าเธอรักฉันจริง",
    "Lipta - ก่อนฤดูฝน",
    "Paradox - ขอ",
    "Getsunova - ความเงียบดังที่สุด",
    "Season Five - นอนจับมือกันครั้งแรก",
    "INK WARUNTORN - เหงา เหงา",
    "Polycat - เวลาเธอยิ้ม"
] * 5)

tired_songs = create_song_list([
    "Bodyslam - ความเชื่อ",
    "Potato - ทิ้งไว้กลางทาง",
    "Cocktail - คุกเข่า",
    "Stamp - มันคงเป็นความรัก",
    "Safeplanet - คำตอบ",
    "Three Man Down - ฝนตกไหม",
    "Getsunova - คนไม่จำเป็น",
    "Room39 - เป็นทุกอย่าง",
    "Lipta - แค่รู้ว่ารัก",
    "Boyd Kosiyabong - รักคุณเข้าแล้ว"
] * 5)

bored_songs = create_song_list([
    "Phum Viphurit - Lover Boy",
    "Scrubb - ทุกอย่าง",
    "Tattoo Colour - ขาหมู",
    "Slot Machine - เคลิ้ม",
    "Paradox - ฤดูร้อน",
    "Lipta - แฟน",
    "Ink Waruntorn - ดีใจด้วยนะ",
    "Safeplanet - ดวงจันทร์กลางวัน",
    "LANDOKMAI - เพลงรักเพลงแรก",
    "Singto Numchok - อยู่ต่อเลยได้ไหม"
] * 5)

heartbreak_songs = create_song_list([
    "Billkin - กีดกัน",
    "Getsunova - ไกลแค่ไหนคือใกล้",
    "Bodyslam - แสงสุดท้าย",
    "Musketeers - แค่คุณ",
    "Season Five - ต่อให้",
    "Potato - เธอยัง",
    "Cocktail - เธอทำให้ฉันเสียใจ",
    "Stamp - ความคิด",
    "Three Man Down - ถ้าเราเจอกันอีก",
    "Lipta - แฟนเก่า"
] * 5)

music_data = {
    "love": love_songs,
    "tired": tired_songs,
    "bored": bored_songs,
    "heartbreak": heartbreak_songs
}

# =============================
# วิเคราะห์อารมณ์ใหม่
# =============================
def detect_mood(text):
    text = text.lower()

    if any(w in text for w in ["อินเลิฟ","รัก","มีความรัก","แฟน"]):
        return "love"
    elif any(w in text for w in ["เหนื่อย","ท้อ","หมดแรง"]):
        return "tired"
    elif any(w in text for w in ["ง่วง","เบื่อ","เซ็ง"]):
        return "bored"
    elif any(w in text for w in ["อกหัก","เศร้า","เสียใจ"]):
        return "heartbreak"
    else:
        return "bored"

# =============================
# Session State
# =============================
if "playlist" not in st.session_state:
    st.session_state.playlist = []
    st.session_state.index = 0
    st.session_state.current_mood = None
    st.session_state.stats = {
        "love":0,
        "tired":0,
        "bored":0,
        "heartbreak":0
    }

# =============================
# Input
# =============================
user_text = st.text_area("วันนี้คุณรู้สึกยังไง?")

if st.button("🤖 วิเคราะห์อารมณ์"):
    if user_text.strip():
        mood = detect_mood(user_text)

        mood_label = {
            "love":"💕 อินเลิฟ / มีความรัก",
            "tired":"😩 เหนื่อย / ท้อ",
            "bored":"😴 ง่วง / เบื่อ",
            "heartbreak":"💔 อกหัก / เศร้า"
        }

        st.success(f"อารมณ์ของคุณคือ: {mood_label[mood]}")

        st.session_state.stats[mood] += 1

        if st.session_state.current_mood != mood:
            st.session_state.playlist = random.sample(music_data[mood], 50)
            st.session_state.index = 0
            st.session_state.current_mood = mood

# =============================
# สุ่มเพลง
# =============================
if st.session_state.current_mood:

    if st.button("🎵 สุ่มเพลง"):
        if st.session_state.index >= 50:
            st.session_state.playlist = random.sample(
                music_data[st.session_state.current_mood], 50
            )
            st.session_state.index = 0
            st.info("ครบ 50 เพลงแล้ว กำลังสับใหม่ 🔄")

        song = st.session_state.playlist[st.session_state.index]
        st.session_state.index += 1

        st.markdown(f"""
        <div class="card">
            <h3>{song['title']}</h3>
            <a href="{song['link']}" target="_blank">🔗 เปิดใน YouTube</a>
            <div class="counter">เพลงที่ {st.session_state.index} / 50</div>
        </div>
        """, unsafe_allow_html=True)

        st.video(song["embed"])

# =============================
# สถิติ
# =============================
st.markdown("## 📊 สถิติอารมณ์ผู้ใช้")

df = pd.DataFrame(
    st.session_state.stats.items(),
    columns=["Mood","Count"]
)

st.bar_chart(df.set_index("Mood"))
