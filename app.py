import streamlit as st
import time
import json
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

# Custom CSS for Premium Look
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
    .highlight-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #1e1e24;
        border-left: 5px solid #2e7d32;
        margin-bottom: 15px;
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
# KAMUS SINEMATOGRAFI (INJECTION ENGINE DATA)
# =====================================================================
CINEMA_DATABASE = {
    "Commercial Ads": {
        "camera": "ARRI Alexa Mini LF",
        "lens": "Panavision Primo Primes",
        "lighting": "High-key commercial lighting, soft diffuse shadows, pristine color grading",
        "style": "Premium commercial aesthetic, crisp textures, ultra-detailed micro-details",
        "extra": "Vibrant colors, high-end brand feel, sleek camera movements"
    },
    "Cinematic Movie (Layar Lebar)": {
        "camera": "RED V-Raptor XL",
        "lens": "85mm Anamorphic Lens",
        "lighting": "Chiaroscuro lighting, dramatic side-lit key light, deep shadows",
        "style": "Hollywood feature film aesthetic, cinematic film grain, subtle lens flare",
        "extra": "Highly emotional depth, anamorphic bokeh, letterbox 2.39:1 aspect ratio"
    },
    "Hyperrealistic Documentary": {
        "camera": "Sony FX9",
        "lens": "35mm Cine Lens",
        "lighting": "Natural golden hour sunlight, authentic environment ambient lighting",
        "style": "National Geographic style, true-to-life skin textures, sharp focus tracking",
        "extra": "No artificial filters, raw organic details, high dynamic range"
    },
    "UGC Viral Masterpiece": {
        "camera": "Blackmagic Pocket Cinema Camera 6K Pro",
        "lens": "24mm Wide-Angle Lens",
        "lighting": "Dynamic practical lights, punchy neon contrast, localized rim lighting",
        "style": "High-engagement viral framing, clean handheld stabilization effect",
        "extra": "Intense visual hooks, fast-paced atmosphere, immersive depth-of-field"
    }
}

# =====================================================================
# SIDEBAR NAVIGATION & SETTINGS
# =====================================================================
with st.sidebar:
    st.title("🎬 Vision Engine Pro")
    st.caption("Content Automation & Cinematic Upscaler")
    st.markdown("---")
    
    # Credit Dashboard Metric
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(label="Sisa Kredit API", value=f"{st.session_state.credits} PTS")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(" ")
    
    menu = st.radio("Navigasi Fitur:", ["1. Extract & Upscale Prompt", "2. Auto-Extension Video Flow", "3. Riwayat Projek"])
    
    st.markdown("---")
    st.markdown("### ⚙️ Master Engine Config")
    api_provider = st.selectbox("API Video Provider:", ["Kling AI API", "Runway Gen-3 API", "Luma Dream Machine API"])
    resolution = st.selectbox("Output Resolution:", ["1080p (FHD)", "4K Ultra HD"])
    aspect_ratio = st.selectbox("Aspect Ratio:", ["9:16 (Reels/TikTok)", "16:9 (Landscape)"])

# =====================================================================
# FEATURE 1: EXTRACT & UPSCALE PROMPT (INJECTION ENGINE)
# =====================================================================
if menu == "1. Extract & Upscale Prompt":
    st.header("⚡ Reverse-Engineering & Cinematic Prompt Extractor")
    st.subheader("Ubah Video Viral Menjadi Prompt Kelas Dunia Tanpa 'AI Slop'")
    
    # Input Methods Tabs
    tab1, tab2 = st.tabs(["🔗 Tempel Link Video (Frictionless)", "📤 Unggah File Video"])
    
    video_source = ""
    with tab1:
        video_url = st.text_input("Masukkan URL Video (TikTok / Instagram Reels / YouTube Shorts):", 
                                 placeholder="https://www.tiktok.com/@viral_user/video/...")
        if video_url:
            video_source = video_url
            st.success("Link berhasil dikunci! Sistem siap melakukan pengunduhan otomatis di background.")
            
    with tab2:
        uploaded_file = st.file_uploader("Pilih file video referensi:", type=["mp4", "mov", "avi"])
        if uploaded_file:
            video_source = uploaded_file.name
            
    st.markdown("---")
    st.header("🎨 AI Cinematographer Injector Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        visual_style = st.selectbox("Pilih Target Gaya Visual (Visual Style Layer):", list(CINEMA_DATABASE.keys()))
        focal_length = st.selectbox("Opsi Lensa & Kedalaman (Focal Length):", 
                                    ["Close-up Emosional (85mm, Shallow DOF)", 
                                     "Medium Shot Seimbang (50mm, Balanced DOF)", 
                                     "Wide-Angle Sinematik (24mm, Deep Focus)"])
    with col2:
        motion_speed = st.slider("Intensitas Gerakan Kamera (Motion Layer):", 1, 5, 3)
        magic_toggle = st.checkbox("Aktifkan 'Magic Enhancement Mode' (Suntikan Otomatis Lensa & Kamera Mahal)", value=True)

    if st.button("🚀 Ekstrak & Suntik Parameter Sinematik"):
        if not video_source:
            st.error("Silakan masukkan link video atau unggah file video terlebih dahulu.")
        else:
            with st.spinner("🔄 Memotong video menjadi keyframes & menganalisis adegan via Vision AI..."):
                time.sleep(2.5) # Mock Vision processing
                
                # Mock extraction result from Vision AI
                raw_extracted = "Seorang tokoh pria utama mengenakan jaket kulit, menatap tajam ke depan dengan ekspresi intens di dalam ruangan remang-remang bergaya industrial."
                
                # Apply Injection Logic
                selected_config = CINEMA_DATABASE[visual_style]
                
                if magic_toggle:
                    final_prompt = (
                        f"Cinematic medium shot, {raw_extracted} "
                        f"Shot on {selected_config['camera']}, paired with {selected_config['lens']}. "
                        f"{selected_config['lighting']}. {selected_config['style']}, {selected_config['extra']}. "
                        f"Camera motion level {motion_speed}, highly cinematic stabilization, flawless physics, no ai artifacts, 4k resolution."
                    )
                else:
                    final_prompt = f"{raw_extracted} Gaya visual: {visual_style}. Kamera level {motion_speed}."
                
                # Script Copywriting Framework (PAS)
                script_hook = "Bocoran rahasia yang tidak ingin diungkapkan oleh kompetitor Anda..."
                script_body = "Selama ini Anda membuang waktu dengan metode lama yang menguras energi dan biaya."
                script_cta = "Klik tombol di bawah untuk akses blueprint eksklusif ini sekarang sebelum ditutup!"
                
                # Save to state history
                st.session_state.history.append({
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "style": visual_style,
                    "prompt": final_prompt
                })
                
                st.balloons()
                
                # DISPLAY OUTPUT
                st.markdown("### 🔥 HASIL EKSTRAKSI & UPSCALE MASTER PROMPT")
                st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
                st.text_area("📋 Master Prompt (Siap di-copy ke Kling/Runway/Veo):", value=final_prompt, height=150)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("### ✍️ AI Direct-Response Script Generator (Bonus Layer)")
                with st.expander("Lihat Struktur Naskah Video Pendek (PAS Framework)"):
                    st.markdown(f'**🔴 HOOK (0-3 Detik):** *"{script_hook}"*')
                    st.markdown(f'**🟡 PROBLEM & AGITATION:** *"{script_body}"*')
                    st.markdown(f'**🟢 CALL TO ACTION (CTA):** *"{script_cta}"*')

# =====================================================================
# FEATURE 2: AUTOMATED VIDEO EXTENSION FLOW
# =====================================================================
elif menu == "2. Auto-Extension Video Flow":
    st.header("⏳ Automated Video Extension & Rendering Pipeline")
    st.subheader("Eksekusi Loop Otomatis: Generasi Per 8 Detik Hingga Mencapai 1 Menit")
    
    if not st.session_state.history:
        st.warning("⚠️ Belum ada prompt sinematik yang di-generate. Silakan masuk ke menu '1. Extract & Upscale Prompt' terlebih dahulu atau masukkan prompt manual di bawah.")
        user_prompt = st.text_area("Masukkan Prompt Sinematik Anda secara manual:", 
                                   value="Cinematic shot on ARRI Alexa, a futuristic sports car driving through neon-lit streets...")
    else:
        user_prompt = st.text_area("Prompt Sinematik Aktif (Diambil dari sesi terakhir):", 
                                   value=st.session_state.history[-1]["prompt"])
        
    st.markdown("---")
    st.markdown("### 📊 Estimasi Pemakaian Kredit Pipeline")
    
    target_duration = st.slider("Target Durasi Video Akhir:", 8, 64, 32, step=8)
    total_loops = target_duration // 8
    required_credits = total_loops * 10
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Jumlah Siklus Loop (8s/loop)", f"{total_loops} Siklus")
    with c2:
        st.metric("Total Kredit yang Dibutuhkan", f"{required_credits} PTS")
    with c3:
        status_credit = "Kredit Cukup" if st.session_state.credits >= required_credits else "Kredit Kurang"
        st.metric("Status Saldo Anda", status_credit)
        
    if st.session_state.credits < required_credits:
        st.error("❌ Saldo Kredit API Anda tidak mencukupi untuk menjalankan otomatisasi durasi panjang ini. Silakan top up atau kurangi target durasi.")
    
    if st.button("🎬 Jalankan Engine Otomatisasi Rendering Video"):
        if st.session_state.credits >= required_credits:
            st.session_state.credits -= required_credits
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulated End-to-End API Pipeline Loop
            for i in range(total_loops):
                current_seconds_start = i * 8
                current_seconds_end = (i + 1) * 8
                
                status_text.markdown(f"🎬 **Menjalankan Siklus {i+1}/{total_loops}:** Memproduksi Detik {current_seconds_start} s.d {current_seconds_end}...")
                
                # Simulating API rendering time
                for percent in range(0, 101, 20):
                    time.sleep(0.4)
                    progress_bar.progress(int((i * 100 / total_loops) + (percent / total_loops)))
            
            status_text.markdown("🔄 **Siklus Loop Selesai!** FFmpeg Engine sedang menggabungkan (*stitching*) seluruh klip di background...")
            time.sleep(2.0)
            
            progress_bar.progress(100)
            st.success(f"🎉 Mahakarya Video Berdurasi {target_duration} Detik Berhasil Terbentuk Sempurna!")
            
            # Display Mock Finished Video Video Box
            st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Mock video link for display
            
            st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
            st.markdown(f"### 📋 Manifes Produksi API:")
            st.markdown(f"- **Total Durasi:** {target_duration} Detik")
            st.markdown(f"- **Metode Penyambungan:** Auto-Extend Last Frame (Detik ke-8)")
            st.markdown(f"- **Sisa Saldo Anda Saat Ini:** {st.session_state.credits} PTS")
            st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# FEATURE 3: PROJECT HISTORY
# =====================================================================
elif menu == "3. Riwayat Projek":
    st.header("🗄️ Riwayat Inkubasi Projek & Log Ekstraksi")
    if not st.session_state.history:
        st.info("Belum ada riwayat projek terdeteksi pada sesi ini. Mulailah melakukan ekstraksi pada menu pertama.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.container():
                st.markdown(f"### 📁 Projek #{len(st.session_state.history) - idx} ({item['style']})")
                st.caption(f"Waktu Eksekusi: {item['timestamp']}")
                st.text_area("Prompt Hasil Injeksi:", value=item['prompt'], height=80, key=f"hist_{idx}")
                st.markdown("---")
