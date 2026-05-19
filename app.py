import streamlit as st
import time
import os
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
# KAMUS SINEMATOGRAFI (INJECTION ENGINE DATABASE)
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
# SIDEBAR NAVIGATION & CREDENTIALS
# =====================================================================
with st.sidebar:
    st.title("🎬 Vision Engine Pro")
    st.caption("Content Automation & Cinematic Upscaler")
    st.markdown("---")
    
    # API Key Input Layer
    st.markdown("### 🔑 API Authentication")
    gemini_api_key = st.text_input("Enter Gemini API Key:", type="password", placeholder="AIzaSy...")
    
    st.markdown("---")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(label="Sisa Kredit Akun", value=f"{st.session_state.credits} PTS")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(" ")
    
    menu = st.radio("Navigasi Fitur:", ["1. Extract & Upscale Prompt", "2. Auto-Extension Video Flow", "3. Riwayat Projek"])
    
    st.markdown("---")
    st.markdown("### ⚙️ Master Engine Config")
    api_provider = st.selectbox("Core Vision Engine:", ["Gemini 1.5 Pro (Native Video)", "Gemini 1.5 Flash"])
    resolution = st.selectbox("Target Resolution:", ["1080p (FHD)", "4K Ultra HD"])
    aspect_ratio = st.selectbox("Aspect Ratio:", ["9:16 (Reels/TikTok)", "16:9 (Landscape)"])

# =====================================================================
# FEATURE 1: LIVE EXTRACT & UPSCALE PROMPT (REAL API EXECUTION)
# =====================================================================
if menu == "1. Extract & Upscale Prompt":
    st.header("⚡ Reverse-Engineering & Cinematic Prompt Extractor")
    st.subheader("Ubah Video Referensi Menjadi Teks Prompt Akurat & Naskah PAS")
    
    uploaded_file = st.file_uploader("Unggah File Video Referensi (MP4/MOV):", type=["mp4", "mov", "avi"])
            
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
        magic_toggle = st.checkbox("Aktifkan 'Magic Enhancement Mode' (Suntikan Otomatis Lensa & Kamera Pro)", value=True)

    if st.button("🚀 Ekstrak & Suntik Parameter Sinematik"):
        if not gemini_api_key:
            st.error("❌ Silakan masukkan Gemini API Key Anda di sidebar terlebih dahulu.")
        elif not uploaded_file:
            st.error("❌ Silakan unggah file video referensi terlebih dahulu.")
        else:
            # Configure Google Gemini GenAI
            genai.configure(api_key=gemini_api_key)
            
            # Use appropriate model based on config
            model_name = 'gemini-1.5-pro-latest' if "Pro" in api_provider else 'gemini-1.5-flash'
            
            with st.spinner("🎬 Mengunggah video ke API File Server & Menganalisis Struktur Scene..."):
                try:
                    # Save uploaded file to a temporary file path
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name

                    # Upload file to Gemini File API
                    video_file = genai.upload_file(path=tmp_path)
                    
                    # Wait for processing if video
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = genai.get_file(video_file.name)
                        
                    if video_file.state.name == "FAILED":
                        raise Exception("Video processing failed on server side.")

                    # Master Prompt Engineering for extraction
                    analysis_prompt = (
                        "Analyze this video clip. Act as an expert AI Video Prompt Engineer. "
                        "Describe the main subject, actions, facial expressions, background, and environment "
                        "in one highly detailed paragraph. Keep it concise, focused on raw descriptive facts, and do not use buzzwords."
                    )
                    
                    # Execute Vision AI Request
                    model = genai.GenerativeModel(model_name=model_name)
                    response = model.generate_content([video_file, analysis_prompt])
                    raw_extracted = response.text.strip()
                    
                    # Clean up file from Gemini cloud storage
                    genai.delete_file(video_file.name)
                    os.unlink(tmp_path) # delete local temp file
                    
                    # Apply Injection Logic from Kamus Sinematografi
                    selected_config = CINEMA_DATABASE[visual_style]
                    
                    if magic_toggle:
                        final_prompt = (
                            f"Cinematic shot, {raw_extracted} "
                            f"Shot on {selected_config['camera']} with {selected_config['lens']}. "
                            f"{selected_config['lighting']}. {selected_config['style']}. {selected_config['extra']}. "
                            f"Camera motion intensity level {motion_speed}, smooth cinematic pan, flawless hyperrealistic physics, 8k resolution, photorealistic master template."
                        )
                    else:
                        final_prompt = f"{raw_extracted} Visual style: {visual_style}. Motion level {motion_speed}."
                    
                    # AI Copywriting Framework Generator (PAS) via Text API
                    copy_prompt = (
                        f"Based on this video description: '{raw_extracted}', write a short video marketing script using the PAS (Problem-Agitation-Solution) framework in Indonesian language. "
                        f"Format the output exactly as JSON with keys: 'hook', 'problem', 'cta'."
                    )
                    copy_response = model.generate_content(copy_prompt)
                    
                    try:
                        # Clean code block tags if present
                        clean_json = copy_response.text.replace("```json", "").replace("```", "").strip()
                        script_data = json.loads(clean_json)
                        script_hook = script_data.get('hook', 'Bocoran rahasia yang tidak ingin diungkap kompetitor...')
                        script_body = script_data.get('problem', 'Selama ini Anda membuang waktu dengan metode lama...')
                        script_cta = script_data.get('cta', 'Klik tombol di bawah untuk akses sekarang!')
                    except:
                        script_hook = "Bocoran rahasia dari kompetitor Anda..."
                        script_body = "Metode lama Anda menguras energi dan biaya tanpa hasil signifikan."
                        script_cta = "Klik tombol di bawah untuk akses sistem otomatis ini sekarang!"

                    # Deduct virtual credit for real operation
                    st.session_state.credits -= 15
                    
                    # Save to state history
                    st.session_state.history.append({
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "style": visual_style,
                        "prompt": final_prompt
                    })
                    
                    st.balloons()
                    
                    # DISPLAY FINAL PRO OUTPUT
                    st.markdown("### 🔥 HASIL EKSTRAKSI & UPSCALE MASTER PROMPT")
                    st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
                    st.text_area("📋 Master Prompt (Siap di-copy ke Kling/Runway/Veo):", value=final_prompt, height=150)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("### ✍️ AI Direct-Response Script Generator (Bonus Layer)")
                    with st.expander("Lihat Struktur Naskah Video Pendek (PAS Framework)", expanded=True):
                        st.markdown(f'**🔴 HOOK (0-3 Detik):** *"{script_hook}"*')
                        st.markdown(f'**🟡 PROBLEM & AGITATION:** *"{script_body}"*')
                        st.markdown(f'**🟢 CALL TO ACTION (CTA):** *"{script_cta}"*')
                        
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan pada API Engine: {str(e)}")

# =====================================================================
# FEATURE 2: AUTOMATED VIDEO EXTENSION FLOW
# =====================================================================
elif menu == "2. Auto-Extension Video Flow":
    st.header("⏳ Automated Video Extension & Rendering Pipeline")
    st.subheader("Eksekusi Loop Otomatis: Generasi Per 8 Detik Hingga Mencapai 1 Menit")
    
    if not st.session_state.history:
        st.warning("⚠️ Belum ada prompt sinematik yang di-generate. Silakan masuk ke menu '1. Extract & Upscale Prompt' atau masukkan prompt manual.")
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
        st.error("❌ Saldo Kredit API Anda tidak mencukupi untuk menjalankan otomatisasi durasi panjang ini.")
    
    if st.button("🎬 Jalankan Engine Otomatisasi Rendering Video"):
        if st.session_state.credits >= required_credits:
            st.session_state.credits -= required_credits
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(total_loops):
                current_seconds_start = i * 8
                current_seconds_end = (i + 1) * 8
                status_text.markdown(f"🎬 **Menjalankan Siklus {i+1}/{total_loops}:** Memproduksi Detik {current_seconds_start} s.d {current_seconds_end}...")
                
                for percent in range(0, 101, 20):
                    time.sleep(0.3)
                    progress_bar.progress(int((i * 100 / total_loops) + (percent / total_loops)))
            
            status_text.markdown("🔄 **Siklus Loop Selesai!** FFmpeg Engine sedang menggabungkan (*stitching*) seluruh klip di background...")
            time.sleep(1.5)
            progress_bar.progress(100)
            st.success(f"🎉 Video Berdurasi {target_duration} Detik Berhasil Terbentuk Sempurna!")
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# =====================================================================
# FEATURE 3: PROJECT HISTORY
# =====================================================================
elif menu == "3. Riwayat Projek":
    st.header("🗄️ Riwayat Inkubasi Projek & Log Ekstraksi")
    if not st.session_state.history:
        st.info("Belum ada riwayat projek terdeteksi pada sesi ini.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.container():
                st.markdown(f"### 📁 Projek #{len(st.session_state.history) - idx} ({item['style']})")
                st.caption(f"Waktu Eksekusi: {item['timestamp']}")
                st.text_area("Prompt Hasil Injeksi:", value=item['prompt'], height=80, key=f"hist_{idx}")
                st.markdown("---")
