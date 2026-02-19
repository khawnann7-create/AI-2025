import streamlit as st
import random
import urllib.parse
import pandas as pd

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Never Die (แนะนำเพลงตามความรู้สึก🐱)",
    page_icon="🎵",
    layout="centered"
)

# ===============================
# Pastel UI CSS
# ===============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #ffd6e8, #d6f6ff);
}
.card {
    background: white;
    padding: 25px;
    border-radius: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    margin-top: 20px;
    text-align: center;
}
.title {
    font-size: 26px;
    font-weight: bold;
    color: #ff6fa5;
}
.subtitle {
    color: gray;
}
.counter {
    font-size: 14px;
    color: #888;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# เพลงจริง 50 เพลงต่อหมวด
# ===============================
def create_song_list(song_names):
    songs = []
    for name in song_names:
        query = urllib.parse.quote(name)
        embed = f"https://www.youtube.com/embed?listType=search&list={query}"
        link = f"https://www.youtube.com/results?search_query={query}"
        songs.append({"title": name, "embed": embed, "link": link})
    return songs

happy_songs = create_song_list([
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
] * 5)  # x5 = 50 เพลง

sad_songs = create_song_list([
    "Billkin - กีดกัน",
    "Getsunova - ไกลแค่ไหนคือใกล้",
    "Bodyslam - ความเชื่อ",
    "Musketeers - แค่คุณ",
    "Potato - ทิ้งไว้กลางทาง",
    "Cocktail - คุกเข่า",
    "Stamp - มันคงเป็นความรัก",
    "Three Man Down - ฝนตกไหม",
    "Safeplanet - คำตอบ",
    "Season Five - ต่อให้"
] * 5)

chill_songs = create_song_list([
    "Safeplanet - ดวงจันทร์กลางวัน",
    "Phum Viphurit - Lover Boy",
    "Scrubb - เธอหมุนรอบฉัน",
    "LANDOKMAI - เพลงรักเพลงแรก",
    "Polycat - เวลาเธอยิ้ม",
    "Boyd Kosiyabong - รักคุณเข้าแล้ว",
    "Singto Numchok - อยู่ต่อเลยได้ไหม",
    "Room39 - เป็นทุกอย่าง",
    "Lipta - แค่รู้ว่ารัก",
    "Ink Waruntorn - ดีใจด้วยนะ"
] * 5)

love_songs = create_song_list([
    "NONT TANONT - โต๊ะริม",
    "Bowkylion - วิงวอน",
    "INK WARUNTORN - เหงา เหงา",
    "Season Five - นอนจับมือกันครั้งแรก",
    "Billkin - โคตรพิเศษ",
    "Three Man Down - ถ้าเธอรักฉันจริง",
    "Getsunova - ความเงียบดังที่สุด",
    "Lipta - ก่อนฤดูฝน",
    "Tattoo Colour - เธอไม่อาจเอารักไปจากหัวใจ",
    "Paradox - ขอ"
] * 5)

music_data = {
    "happy": happy_songs,
    "sad": sad_songs,
    "chill": chill_songs,
    "love": love_songs
}

# ===============================
# วิเคราะห์อารมณ์
# ===============================
def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["ดีใจ", "มีความสุข", "สดใส", "สนุก"]):
        return "happy"
    elif any(w in text for w in ["เศร้า", "เสียใจ", "ร้องไห้", "ท้อ"]):
        return "sad"
    elif any(w in text for w in ["รัก", "คิดถึง", "แฟน"]):
        return "love"
    else:
        return "chill"

# ===============================
# Session State
# ===============================
if "playlist" not in st.session_state:
    st.session_state.playlist = []
    st.session_state.index = 0
    st.session_state.current_mood = None
    st.session_state.stats = {"happy":0,"sad":0,"chill":0,"love":0}

# ===============================
# UI
# ===============================
st.markdown("<div class='title'>🐱 Pastel Mood Music</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>พิมพ์ความรู้สึก แล้วให้แมวเลือกเพลงให้ 🎵</div>", unsafe_allow_html=True)

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

# ===============================
# สุ่มเพลง
# ===============================
if st.session_state.current_mood:

    if st.button("🎵 สุ่มเพลง"):
        if st.session_state.index >= 50:
            st.session_state.playlist = random.sample(
                music_data[st.session_state.current_mood], 50
            )
            st.session_state.index = 0
            st.info("ครบ 50 เพลงแล้ว สับใหม่ 🔄")

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

# ===============================
# แสดงสถิติอารมณ์
# ===============================
st.markdown("## 📊 สถิติอารมณ์ผู้ใช้")

df = pd.DataFrame(
    st.session_state.stats.items(),
    columns=["Mood","Count"]
)

st.bar_chart(df.set_index("Mood"))
