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
# Pastel CSS
# =============================
st.markdown("""
<style>

/* Background */
body {
    background: linear-gradient(135deg, #ffd6e8, #d6f6ff);
}

/* Title */
.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #ff6fa5;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 20px;
}

/* Pastel Text Area */
textarea {
    background-color: #fff0f6 !important;
    border-radius: 20px !important;
    border: 2px solid #ffc2d1 !important;
    padding: 10px !important;
}

/* Button */
.stButton>button {
    background-color: #ffb3c6;
    color: white;
    border-radius: 20px;
    border: none;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #ff8fab;
    color: white;
}

/* Card */
.card {
    background: #ffffff;
    padding: 25px;
    border-radius: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    margin-top: 20px;
    text-align: center;
}

/* Counter */
.counter {
    font-size: 14px;
    color: #888;
}

</style>
""", unsafe_allow_html=True)

# =============================
# Header
# =============================
st.markdown("<div class='title'>🎵 Music will never die</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>พิมพ์ความรู้สึก แล้วให้ดนตรีเยียวยาคุณ 💖</div>", unsafe_allow_html=True)

# =============================
# สร้างเพลงจริง 50 เพลง
# =============================
def create_song_list(song_names):
    songs = []
    for name in song_names:
        query = urllib.parse.quote(name)
        embed = f"https://www.youtube.com/embed?listType=search&list={query}"
        link = f"https://www.youtube.com/results?search_query={query}"
        songs.append({"title": name, "embed": embed, "link": link})
    return songs

base_happy = [
    "Lipta - แฟน",
    "Three Man Down - ข้างกัน",
    "Polycat - ดูดี",
    "Scrubb - ทุกอย่าง",
    "Billkin - I ไม่ O",
    "Bodyslam - แสงสุดท้าย",
    "Slot Machine - เคลิ้ม",
    "Tattoo Colour - ขาหมู",
    "Paradox - ฤดูร้อน",
    "Getsunova - คนไม่จำเป็น",
]

base_sad = [
    "Billkin - กีดกัน",
    "Getsunova - ไกลแค่ไหนคือใกล้",
    "Bodyslam - ความเชื่อ",
    "Musketeers - แค่คุณ",
    "Potato - ทิ้งไว้กลางทาง",
    "Cocktail - คุกเข่า",
    "Stamp - มันคงเป็นความรัก",
    "Three Man Down - ฝนตกไหม",
    "Safeplanet - คำตอบ",
    "Season Five - ต่อให้",
]

base_chill = [
    "Safeplanet - ดวงจันทร์กลางวัน",
    "Phum Viphurit - Lover Boy",
    "Scrubb - เธอหมุนรอบฉัน",
    "LANDOKMAI - เพลงรักเพลงแรก",
    "Polycat - เวลาเธอยิ้ม",
    "Boyd Kosiyabong - รักคุณเข้าแล้ว",
    "Singto Numchok - อยู่ต่อเลยได้ไหม",
    "Room39 - เป็นทุกอย่าง",
    "Lipta - แค่รู้ว่ารัก",
    "Ink Waruntorn - ดีใจด้วยนะ",
]

base_love = [
    "NONT TANONT - โต๊ะริม",
    "Bowkylion - วิงวอน",
    "INK WARUNTORN - เหงา เหงา",
    "Season Five - นอนจับมือกันครั้งแรก",
    "Billkin - โคตรพิเศษ",
    "Three Man Down - ถ้าเธอรักฉันจริง",
    "Getsunova - ความเงียบดังที่สุด",
    "Lipta - ก่อนฤดูฝน",
    "Tattoo Colour - เธอไม่อาจเอารักไปจากหัวใจ",
    "Paradox - ขอ",
]

music_data = {
    "happy": create_song_list(base_happy * 5),
    "sad": create_song_list(base_sad * 5),
    "chill": create_song_list(base_chill * 5),
    "love": create_song_list(base_love * 5),
}

# =============================
# วิเคราะห์อารมณ์
# =============================
def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["ดีใจ","มีความสุข","สดใส","สนุก"]):
        return "happy"
    elif any(w in text for w in ["เศร้า","เสียใจ","ร้องไห้","ท้อ"]):
        return "sad"
    elif any(w in text for w in ["รัก","คิดถึง","แฟน"]):
        return "love"
    else:
        return "chill"

# =============================
# Session State
# =============================
if "playlist" not in st.session_state:
    st.session_state.playlist = []
    st.session_state.index = 0
    st.session_state.current_mood = None
    st.session_state.stats = {"happy":0,"sad":0,"chill":0,"love":0}

# =============================
# Input
# =============================
user_text = st.text_area("วันนี้คุณรู้สึกยังไง?")

if st.button("🤖 วิเคราะห์อารมณ์"):
    if user_text.strip():
        mood = detect_mood(user_text)
        st.success(f"อารมณ์ของคุณคือ: {mood.upper()} 💖")
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
