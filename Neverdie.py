import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="Mood Music Cat 🐱", page_icon="🐱")

# ==================================================
# ฟังก์ชันสร้างเพลง 50 เพลงต่ออารมณ์
# ==================================================
def generate_songs(prefix):
    songs = []
    for i in range(1, 51):
        title = f"{prefix} Song {i}"
        query = urllib.parse.quote(title)
        link = f"https://www.youtube.com/results?search_query={query}"
        songs.append({"title": title, "link": link})
    return songs

music_data = {
    "😊 มีความสุข": generate_songs("Happy"),
    "😢 เศร้า": generate_songs("Sad"),
    "😌 ชิล ๆ": generate_songs("Chill"),
    "❤️ ตกหลุมรัก": generate_songs("Love"),
}

# ==================================================
# UI
# ==================================================
st.title("🐱💿 แนะนำเพลงตามความรู้สึก")
st.write("วันนี้คุณรู้สึกยังไงบ้าง?")

mood = st.selectbox("เลือกอารมณ์", list(music_data.keys()))

# ==================================================
# ระบบสุ่มแบบไม่ซ้ำ
# ==================================================
if "playlist" not in st.session_state:
    st.session_state.playlist = []
    st.session_state.index = 0
    st.session_state.current_mood = None

# ถ้าเปลี่ยนอารมณ์ → รีเซ็ต
if st.session_state.current_mood != mood:
    st.session_state.playlist = random.sample(music_data[mood], len(music_data[mood]))
    st.session_state.index = 0
    st.session_state.current_mood = mood

if st.button("🎵 สุ่มเพลง"):
    # ถ้าครบ 50 เพลงแล้ว → สับใหม่
    if st.session_state.index >= len(st.session_state.playlist):
        st.session_state.playlist = random.sample(music_data[mood], len(music_data[mood]))
        st.session_state.index = 0
        st.info("ครบ 50 เพลงแล้ว! กำลังสับใหม่ 🔄")

    song = st.session_state.playlist[st.session_state.index]
    st.session_state.index += 1

    st.subheader("🎶 เพลงที่สุ่มได้")
    st.markdown(f"**{song['title']}**")
    st.markdown(f"[🔗 คลิกฟังเพลงที่นี่]({song['link']})")

    st.write(f"ลำดับที่ {st.session_state.index} / 50 เพลง")

