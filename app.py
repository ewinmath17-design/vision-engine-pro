import streamlit as st
import time
import os
import json
import tempfile
import google.generativeai as genai

# =====================================================================
# CONFIGURATION & PAGE SETUP
# =====================================================================
st.set_page_config(
    page_title="Cinematic Vision AI Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Dark Theme
st.markdown("""
<style>
    .reportview-container { background: #0e1117; }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #1b5e20; border-color: #a1887f; }
    .shot-box {
        background-color: #1e1e24;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #161a22;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2d3748;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'credits' not in st.session_state:
    st.session_state.credits = 500

# =====================================================================
# KAMUS SINEMATOGRAFI
# =====================================================================
CINEMA_DATABASE = {
    "Commercial Ads": "Shot on ARRI Alexa 65, 50mm Prime Lens. Studio high-key lighting. High-end commercial, ultra-detailed, hyperrealistic.",
    "Cinematic Movie": "Shot on RED V-Raptor, 85mm Anamorphic Lens. Chiaroscuro lighting, dramatic shadows. Hollywood blockbuster, film grain.",
    "UGC Viral": "Shot on iPhone 15 Pro Max, 24mm Wide. Natural daylight, dynamic contrast. TikTok viral aesthetic, raw and authentic."
}

# =====================================================================
# SIDEBAR NAVIGATION & API AUTH
# =====================================================================
with st.sidebar:
    st.title("🎬 Vision Engine Pro")
    st.caption("Auto-Storyboard & Keyframe Extractor")
    st.markdown("---")
    
    st.markdown("### 🔑 API Authentication")
    gemini_api_key = st.text_input("Enter Gemini API Key:", type="password")
    
    st.markdown("---")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(label="Sisa Kredit API", value=f"{st.session_state.credits} PTS")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# MAIN ENGINE: AUTO-STORYBOARD EXTRACTOR
# =====================================================================
st.header("⚡ The Pro Workflow: Auto-Storyboard Engine")
st.subheader("Bongkar 1 Video Referensi Menjadi Narasi 3 Shot (Awal - Puncak - Akhir)")

uploaded_file = st.file_uploader("Unggah File Video Referensi (MP4/MOV):", type=["mp4", "mov", "avi"])

st.markdown("---")
st.header("🎨 Cinematic Upscale Settings")
col1, col2 = st.columns(2)
with col1:
    visual_style = st.selectbox("Pilih Target Gaya Visual:", list(CINEMA_DATABASE.keys()))
with col2:
    motion_speed = st.selectbox("Intensitas Gerakan Kamera (Motion):", ["Smooth & Cinematic", "Dynamic & Fast", "Slow Push-in"])

if st.button("🚀 Ekstrak & Buat Storyboard (Live API)"):
    if not gemini_api_key:
        st.error("❌ Masukkan Gemini API Key di sidebar kiri terlebih dahulu.")
    elif not uploaded_file:
        st.error("❌ Unggah file video terlebih dahulu.")
    else:
        try:
            genai.configure(api_key=gemini_api_key)
            # Menggunakan model terbaru yang valid untuk mencegah 404 Error
            model = genai.GenerativeModel('gemini-1.5-pro-latest') 
            
            with st.spinner("🎬 Mengunggah video ke AI Server & Merancang Storyboard... (Bisa memakan waktu 1-2 menit)"):
                
                # 1. Simpan file sementara
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                # 2. Upload ke Gemini
                video_file = genai.upload_file(path=tmp_path)
                
                # Tunggu proses processing di server Google
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                
                if video_file.state.name == "FAILED":
                    raise Exception("Gagal memproses video di server AI.")

                # 3. Master Prompt untuk Auto-Storyboard
                system_prompt = f"""
                Analyze this video clip. It is a single scene. I want to expand it into a 3-shot storytelling sequence for a video ad.
                - Shot 1: The Setup/Problem (Before the uploaded scene).
                - Shot 2: The Climax/Action (The exact scene uploaded).
                - Shot 3: The Resolution/Ending (After the uploaded scene).
                
                For each shot, provide two things:
                1. 'start_frame': A highly detailed image prompt describing the subject and background.
                2. 'motion': The camera movement instruction.
                
                Output STRICTLY in JSON format like this:
                {{
                    "shot_1": {{"start_frame": "...", "motion": "..."}},
                    "shot_2": {{"start_frame": "...", "motion": "..."}},
                    "shot_3": {{"start_frame": "...", "motion": "..."}}
                }}
                """
                
                # 4. Generate Konten
                response = model.generate_content([video_file, system_prompt])
                
                # 5. Bersihkan File & Parse JSON
                genai.delete_file(video_file.name)
                os.unlink(tmp_path)
                
                raw_json = response.text.replace("```json", "").replace("```", "").strip()
                storyboard = json.loads(raw_json)
                
                # Kurangi kredit
                st.session_state.credits -= 25
                st.success("✅ Auto-Storyboard Berhasil Diciptakan!")
                
                base_cinema = CINEMA_DATABASE[visual_style]
                
                # 6. Tampilkan Hasil (Shot 1, 2, 3)
                for shot_num in ["shot_1", "shot_2", "shot_3"]:
                    shot_title = "🎬 SHOT 1: SETUP (AWAL/MASALAH)" if shot_num == "shot_1" else "🎬 SHOT 2: CLIMAX (PUNCAK/ADEGAN ASLI)" if shot_num == "shot_2" else "🎬 SHOT 3: RESOLUTION (AKHIR/SOLUSI)"
                    
                    st.markdown(f"<div class='shot-box'>", unsafe_allow_html=True)
                    st.markdown(f"### {shot_title}")
                    
                    st.markdown("**🟢 START FRAME (Gunakan di Text-to-Image):**")
                    st.code(f"{storyboard[shot_num]['start_frame']} {base_cinema}", language="text")
                    
                    st.markdown("**🎥 MOTION PROMPT (Gunakan di Luma/Kling/Veo):**")
                    st.code(f"{storyboard[shot_num]['motion']} Style: {motion_speed}.", language="text")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                st.info("💡 **TIPS PRO:** Generate foto untuk ketiga 'Start Frame' di atas, lalu masukkan foto-foto tersebut beserta 'Motion Prompt'-nya ke Veo/Kling untuk dirangkai menjadi video utuh!")

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan Sistem API: {str(e)}")
