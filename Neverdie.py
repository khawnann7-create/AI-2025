import streamlit as st
import random
import urllib.parse
from textblob import TextBlob

st.set_page_config(page_title="Mood Music AI 🐱", page_icon="🐱", layout="centered")

# ==================================================
# CSS การ์ดสวย ๆ
# ==================================================
st.markdown("""
<style>
.card {
    background: linear-gradient(135deg, #ffe0f0, #e0f7fa);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    margin-top: 20px;
}
.title {
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# สร้างเพลง 50 เพลงต่ออารมณ์
# ==================================================
def generate_songs(prefix):
    songs = []
    for i in range(1, 51):
        title = f"{prefix} Song {i}"
        query = urllib.parse.quote(title)
        youtube_link = f"https://www.youtube.com/results?search_query={query}"
        embed_link = f"https://www.youtube.com/embed?listType=search&list={query}"
        songs.append({
            "title": title,
            "link": youtube_link,
            "embed": embed_link
        })
    return songs

music_data = {
    "happy": generate_songs("Happy"),
    "sad": generate_songs("Sad"),
    "chill": generate_songs("Chill"),
    "love": generate_songs("Love"),
}

# ==================================================
# AI วิเคราะห์อารมณ์
# ==================================================
def detect_mood(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    elif "love" in text.lower():
        return "love"
    else:
        return "chill"

# ==================================================
# UI
# ==================================================
st.title("🐱💿 AI แนะนำเพลงตามความรู้สึก")
st.write("พิมพ์ข้อความ แล้ว AI จะวิเคราะห์อารมณ์ให้ 🎯")

user_text = st.text_area("วันนี้คุณรู้สึกยังไง?")

if st.button("🤖 วิเคราะห์อารมณ์"):
    if user_text.strip() != "":
        mood = detect_mood(user_text)
        st.success(f"AI วิเคราะห์ว่าอารมณ์ของคุณคือ: {mood.upper()} 💖")
    else:
        st.warning("กรุณาพิมพ์ข้อความก่อน")

# ==================================================
# ระบบสุ่มเพลง
# ==================================================
if "playlist" not in st.session_state:
    st.session_state.playlist = []
    st.session_state.index = 0
    st.session_state.current_mood = None

if user_text.strip() != "":
    mood = detect_mood(user_text)

    if st.session_state.current_mood != mood:
        st.session_state.playlist = random.sample(music_data[mood], 50)
        st.session_state.index = 0
        st.session_state.current_mood = mood

    if st.button("🎵 สุ่มเพลงให้หน่อย"):
        if st.session_state.index >= 50:
            st.session_state.playlist = random.sample(music_data[mood], 50)
            st.session_state.index = 0
            st.info("ครบ 50 เพลงแล้ว! สับใหม่ 🔄")

        song = st.session_state.playlist[st.session_state.index]
        st.session_state.index += 1

        # การ์ดแสดงเพลง
        st.markdown(f"""
        <div class="card">
            <div class="title">🎶 {song['title']}</div>
            <br>
            <a href="{song['link']}" target="_blank">🔗 เปิดใน YouTube</a>
        </div>
        """, unsafe_allow_html=True)

        # ฝัง YouTube Player
        st.video(song["embed"])

        st.write(f"ลำดับที่ {st.session_state.index} / 50 เพลง")

