import os
import google.generativeai as genai
from pypdf import PdfReader
import streamlit as st
from prompt import PROMPT_WORKAW
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import dotenv

# โหลด Environment Variables
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# ตั้งค่า API Key
if not GOOGLE_API_KEY:
    st.error("ไม่พบ GOOGLE_API_KEY ในไฟล์ .env")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# ตั้งค่าการตอบ
generation_config = {
    "temperature": 0.0, 
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

# --- ส่วนอ่านไฟล์ PDF ---
pdf_filename = "Graphic.pdf" 
pdf_content = ""

try:
    if os.path.exists(pdf_filename):
        reader = PdfReader(pdf_filename)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_content += text + "\n"
        print(f"✅ อ่านไฟล์สำเร็จ! ความยาว: {len(pdf_content)} ตัวอักษร")
    else:
        st.error(f"❌ ไม่พบไฟล์ {pdf_filename}")
except Exception as e:
    st.error(f"❌ Error: {e}")

# --- รวม Prompt ---
FULL_SYSTEM_INSTRUCTION = f"""
{PROMPT_WORKAW}
CONTEXT:
{pdf_content}
"""

# สร้าง Model (ใช้ 1.5-flash เพื่อความเสถียร)
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        safety_settings=SAFETY_SETTINGS,
        generation_config=generation_config,
        system_instruction=FULL_SYSTEM_INSTRUCTION 
    )
except:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        safety_settings=SAFETY_SETTINGS,
        generation_config=generation_config
    )

# --- 🔥 [NEW] ส่วนตกแต่งสีสันสวยงาม (Teawit69 Theme) 🔥 ---
st.markdown("""
<style>
/* 1. พื้นหลังแบบไล่เฉดสี Sunset Ocean */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #f1c40f 100%);
    background-attachment: fixed;
}

/* 2. ลายแผนที่จางๆ ทับพื้นหลัง */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: url("https://www.transparenttextures.com/patterns/old-map.png");
    opacity: 0.2;
    z-index: -1;
}

/* 3. ปรับกรอบข้อความ Chat (Glassmorphism) */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(8px);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 10px;
}

/* 4. ปรับสีตัวหนังสือให้เด่นบนพื้นหลังเข้ม */
[data-testid="stChatMessage"] p, .stMarkdown p {
    color: #ffffff !important;
}

/* 5. Sidebar แบบโปร่งใส */
[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.4) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255, 215, 0, 0.2);
}

/* 6. หัวข้อ Teawit69 แบบเรืองแสง */
h1 {
    color: #f1c40f !important;
    text-shadow: 0 0 15px rgba(241, 196, 15, 0.9), 2px 2px 5px #000;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
}

/* 7. ปรับสีปุ่ม */
.stButton>button {
    background-color: #e67e22 !important;
    color: white !important;
    border-radius: 20px !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- User Interface ---
def clear_history():
    st.session_state["messages"] = [
        {"role": "model", "content": "ยินดีต้อนรับกลับมาครับกัปตัน Teawit69! พร้อมออกเรือหาความรู้กราฟิกหรือยังครับ? 🏴‍☠️✨"}
    ]
    st.rerun()

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/a/af/One_Piece_Carnival_Logo.png/250px-One_Piece_Carnival_Logo.png")
    if st.button("🗑️ ล้างบันทึกการเดินทาง"):
        clear_history()

# ชื่อโปรเจกต์
st.title("⚓ Teawit69")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "model", "content": "ยินดีต้อนรับกลับมาครับกัปตัน Teawit69! พร้อมออกเรือหาความรู้กราฟิกหรือยังครับ? 🏴‍☠️✨"}
    ]

# แสดงประวัติ
for msg in st.session_state["messages"]:
    avatar_icon = "🍖" if msg["role"] == "user" else "👒"
    st.chat_message(msg["role"], avatar=avatar_icon).write(msg["content"])

# รับ Input
if prompt := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🍖").write(prompt)

    def generate_response():
        history_api = [
            {"role": msg["role"], "parts": [{"text": msg["content"]}]}
            for msg in st.session_state["messages"]
        ]

        try:
            chat_session = model.start_chat(history=history_api)
            
            # บังคับตอบตามเอกสาร
            strict_prompt = f"""
            {prompt}
            
            (COMMAND: Answer ONLY based on the CONTEXT provided. 
            If not found, say 'ขออภัยครับกัปตัน ข้อมูลนี้ไม่ได้อยู่ในบันทึกการเดินทางของเราครับ 🌊')
            """
            
            response = chat_session.send_message(strict_prompt)
            
            st.session_state["messages"].append({"role": "model", "content": response.text})
            st.chat_message("model", avatar="👒").write(response.text)

        except Exception as e:
            st.error(f"เกิดพายุลมแรง! ระบบขัดข้อง: {e}")

    generate_response()