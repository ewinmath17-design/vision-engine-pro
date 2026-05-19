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
    gemini_api_key = st.text_input("Enter Gemini API Key (Untuk File Upload):", type="password")
    
    st.markdown("---")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(label="Sisa Kredit API", value=f"{st.session_state.credits} PTS")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# MAIN ENGINE: AUTO-STORYBOARD EXTRACTOR
# =====================================================================
st.header("⚡ The Pro Workflow: Auto-Storyboard Engine")
st.subheader("Bongkar Video Referensi Menjadi Narasi 3 Shot (Awal - Puncak - Akhir)")

# Frictionless Entry: Tabs for Link vs Upload
tab1, tab2 = st.tabs(["🔗 Tempel Link Video (Frictionless)", "📤 Unggah File Video (Deep AI Analysis)"])

video_url = None
uploaded_file = None

with tab1:
    video_url = st.text_input("Masukkan URL Video (TikTok / Instagram Reels / YouTube Shorts):", 
                              placeholder="https://www.tiktok.com/@viral_user/video/...")
    if video_url:
        st.success("✅ Link berhasil dikunci! Sistem siap melakukan rendering cerdas.")
        
with tab2:
    uploaded_file = st.file_uploader("Atau unggah file video referensi (MP4/MOV):", type=["mp4", "mov", "avi"])
    if uploaded_file:
        st.success(f"✅ File {uploaded_file.name} siap dianalisis oleh AI.")

st.markdown("---")
st.header("🎨 Cinematic Upscale Settings")
col1, col2 = st.columns(2)
with col1:
    visual_style = st.selectbox("Pilih Target Gaya Visual:", list(CINEMA_DATABASE.keys()))
with col2:
    motion_speed = st.selectbox("Intensitas Gerakan Kamera (Motion):", ["Smooth & Cinematic", "Dynamic & Fast", "Slow Push-in"])

if st.button("🚀 Ekstrak & Buat Storyboard"):
    if not video_url and not uploaded_file:
        st.error("❌ Silakan masukkan link video atau unggah file video terlebih dahulu.")
    elif uploaded_file and not gemini_api_key:
        st.error("❌ Masukkan Gemini API Key di sidebar kiri untuk memproses file video asli.")
    else:
        try:
            with st.spinner("🎬 Memproses referensi & merancang Storyboard... (Bisa memakan waktu 1-2 menit)"):
                
                storyboard = {}
                
                # -------------------------------------------------------------
                # JALUR 1: JIKA MENGUNGGAH FILE (MENGGUNAKAN API ASLI)
                # -------------------------------------------------------------
                if uploaded_file:
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel('gemini-1.5-pro-latest') 
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name

                    video_file = genai.upload_file(path=tmp_path)
                    
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = genai.get_file(video_file.name)
                    
                    if video_file.state.name == "FAILED":
                        raise Exception("Gagal memproses video di server AI.")

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
                    
                    response = model.generate_content([video_file, system_prompt])
                    genai.delete_file(video_file.name)
                    os.unlink(tmp_path)
                    
                    raw_json = response.text.replace("```json", "").replace("```", "").strip()
                    storyboard = json.loads(raw_json)
                
                # -------------------------------------------------------------
                # JALUR 2: JIKA MENEMPELKAN LINK (DEMO FAST-ENGINE)
                # -------------------------------------------------------------
                elif video_url:
                    time.sleep(3) # Simulasi scraping dan analisis
                    storyboard = {
                        "shot_1": {
                            "start_frame": "Suasana awal yang suram, karakter utama menatap kosong ke arah kamera dengan latar belakang jalanan yang basah setelah hujan.",
                            "motion": "Kamera melakukan pergerakan perlahan mendekati wajah karakter (slow push-in), menciptakan ketegangan."
                        },
                        "shot_2": {
                            "start_frame": "Karakter utama menemukan solusi, ekspresi wajah berubah menjadi terkejut dan antusias, memegang sebuah produk digital bercahaya.",
                            "motion": "Kamera berputar perlahan mengelilingi karakter (orbit shot) sambil menyorot perubahan emosi."
                        },
                        "shot_3": {
                            "start_frame": "Karakter tersenyum puas dan percaya diri, langit di latar belakang mulai cerah dengan sinar matahari keemasan menerobos awan.",
                            "motion": "Kamera bergerak mundur secara bertahap (pull-back shot) memperlihatkan keseluruhan pemandangan yang megah."
                        }
                    }

                # Kurangi kredit
                st.session_state.credits -= 25
                st.success("✅ Auto-Storyboard Berhasil Diciptakan!")
                
                base_cinema = CINEMA_DATABASE[visual_style]
                
                # Render Hasil (Shot 1, 2, 3)
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
            st.error(f"❌ Terjadi kesalahan Sistem: {str(e)}")
