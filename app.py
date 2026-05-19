import streamlit as st
import time
import random

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
    .prompt-box {
        background-color: #1e1e24;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 15px;
        font-family: monospace;
        font-size: 14px;
        color: #e0e0e0;
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
if 'history' not in st.session_state:
    st.session_state.history = []

# =====================================================================
# KAMUS SINEMATOGRAFI (INJECTION ENGINE DATABASE)
# =====================================================================
CINEMA_DATABASE = {
    "Commercial Ads": {
        "camera": "ARRI Alexa 65",
        "lens": "50mm Prime Lens",
        "lighting": "Studio high-key lighting, softboxes, pristine color grading",
        "style": "High-end commercial, ultra-detailed, hyperrealistic"
    },
    "Cinematic Movie (Layar Lebar)": {
        "camera": "RED V-Raptor",
        "lens": "85mm Anamorphic Lens",
        "lighting": "Chiaroscuro lighting, dramatic shadows, neon rim light",
        "style": "Hollywood blockbuster, film grain, anamorphic flares"
    },
    "UGC Viral Masterpiece": {
        "camera": "iPhone 15 Pro Max",
        "lens": "24mm Wide",
        "lighting": "Natural daylight, dynamic contrast",
        "style": "TikTok viral aesthetic, raw and authentic, engaging"
    }
}

# =====================================================================
# SIDEBAR NAVIGATION
# =====================================================================
with st.sidebar:
    st.title("🎬 Vision Engine Pro")
    st.caption("Structured Prompt Extractor for Kling/Luma/Veo")
    st.markdown("---")
    
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(label="Sisa Kredit Prompt", value=f"{st.session_state.credits} PTS")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = st.radio("Navigasi Fitur:", ["1. Extract Keyframe Prompts", "2. Riwayat Projek"])

# =====================================================================
# FEATURE 1: EXTRACT KEYFRAME PROMPTS (THE "OPSI B" FLOW)
# =====================================================================
if menu == "1. Extract Keyframe Prompts":
    st.header("⚡ Keyframe Prompt Extractor")
    st.subheader("Bongkar Video Menjadi Prompt Awal (Mulai) & Akhir Untuk Tools AI Video")
    
    # Frictionless Entry: Tabs for Link vs Upload
    tab1, tab2 = st.tabs(["🔗 Tempel Link Video (Frictionless)", "📤 Unggah File Video"])
    
    video_source = None
    
    with tab1:
        video_url = st.text_input("Masukkan URL Video (TikTok / Instagram Reels / YouTube Shorts):", 
                                 placeholder="https://www.tiktok.com/@viral_user/video/...")
        if video_url:
            video_source = video_url
            st.success("✅ Link berhasil dikunci! Sistem siap melakukan rendering.")
            
    with tab2:
        uploaded_file = st.file_uploader("Atau unggah file video referensi (MP4/MOV):", type=["mp4", "mov", "avi"])
        if uploaded_file:
            video_source = uploaded_file.name
            st.success(f"✅ File {video_source} siap dianalisis.")
            
    st.markdown("---")
    st.header("🎨 Cinematic Upscale Injector")
    
    col1, col2 = st.columns(2)
    with col1:
        visual_style = st.selectbox("Pilih Target Gaya Visual (Menentukan Kamera & Lensa):", list(CINEMA_DATABASE.keys()))
    with col2:
        motion_speed = st.selectbox("Intensitas Gerakan Kamera (Motion Layer):", ["Slow & Smooth (Cinematic)", "Dynamic & Fast (Action)", "Static (No Camera Move)"])

    if st.button("🚀 Ekstrak Struktur Prompt (Mulai ➔ Motion ➔ Akhir)"):
        if not video_source:
            st.error("❌ Silakan masukkan link video atau unggah file video terlebih dahulu.")
        else:
            with st.spinner("🎬 Mengunduh referensi & membedah struktur video menjadi Keyframe Awal dan Akhir..."):
                time.sleep(2.5) # Simulasi processing time (downloading & extracting)
                
                # Mengambil data dari Kamus Sinematografi
                config = CINEMA_DATABASE[visual_style]
                base_cinema_injection = f"Shot on {config['camera']} with {config['lens']}. {config['lighting']}. {config['style']}."
                
                # Simulasi Hasil Ekstraksi AI Vision
                start_scene = "Seorang pria berdiri di tengah jalanan kota yang kosong, menatap ke arah langit yang mendung."
                end_scene = "Pria tersebut tersenyum tipis saat sinar matahari mulai menembus awan dan menyinari wajahnya."
                action_desc = "Kamera perlahan melakukan push-in (mendekat) ke wajah pria tersebut, transisi cuaca dari mendung menjadi cerah."
                
                # Merangkai Prompt Akhir
                prompt_start = f"IMAGE 1 (START FRAME):\n{start_scene} {base_cinema_injection}"
                prompt_motion = f"VIDEO PROMPT (MOTION & ACTION):\n{action_desc} Camera movement: {motion_speed}."
                prompt_end = f"IMAGE 2 (END FRAME):\n{end_scene} {base_cinema_injection}"
                
                # Potong kredit
                st.session_state.credits -= 5
                
                st.success("✅ Ekstraksi Berhasil! Salin prompt di bawah ini ke Kling / Luma / Veo Anda.")
                
                # TAMPILAN OUTPUT TERSTRUKTUR
                st.markdown("### 🟢 1. START FRAME (Gambar Awal)")
                st.info("Gunakan prompt ini di fitur 'Text-to-Image' atau kolom 'Start Image' untuk membuat awalan video.")
                st.code(prompt_start, language="text")
                
                st.markdown("### 🎥 2. MOTION & ACTION PROMPT")
                st.info("Masukkan prompt ini di kolom 'Video Prompt' / 'Text-to-Video' untuk mengarahkan pergerakan AI.")
                st.code(prompt_motion, language="text")
                
                st.markdown("### 🏁 3. END FRAME (Gambar Akhir / Opsional)")
                st.info("Gunakan prompt ini jika tool AI Anda (seperti Luma Dream Machine) memiliki fitur 'End Frame'.")
                st.code(prompt_end, language="text")
                
                # Simpan ke riwayat
                st.session_state.history.append({
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "style": visual_style,
                    "start": prompt_start,
                    "motion": prompt_motion,
                    "end": prompt_end
                })

# =====================================================================
# FEATURE 2: PROJECT HISTORY
# =====================================================================
elif menu == "2. Riwayat Projek":
    st.header("🗄️ Riwayat Ekstraksi Keyframe")
    if not st.session_state.history:
        st.info("Belum ada riwayat projek terdeteksi.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"📁 Projek #{len(st.session_state.history) - idx} - {item['style']} ({item['timestamp']})"):
                st.markdown("**START FRAME:**")
                st.code(item['start'], language="text")
                st.markdown("**MOTION:**")
                st.code(item['motion'], language="text")
                st.markdown("**END FRAME:**")
                st.code(item['end'], language="text")
