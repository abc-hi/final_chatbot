

# # Frontend

import streamlit as st
import requests
import base64

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="RAG Career Assistant", layout="wide")

# =========================
# IMAGE ENCODING FUNCTION
# =========================
def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

main_bg = get_base64("Data/brandon-griggs-Sp3Nt30ir-U-unsplash.jpg")
sidebar_bg = get_base64("Data/plufow-le-studio-X9X0MBr0tsQ-unsplash.jpg")

# =========================
# BACKGROUND STYLING (FIXED ONLY HERE)
# =========================
st.markdown(f"""
<style>

/* ================= FULL HEIGHT FIX ================= */
html, body, [data-testid="stAppViewContainer"] {{
    height: 100vh !important;
    min-height: 100vh !important;
    margin: 0;
    padding: 0;
}}

/* MAIN BACKGROUND */
.stApp {{
    background-image: url("data:image/jpg;base64,{main_bg}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 100vh !important;
}}

/* FIX OVERLAY TO COVER FULL SCREEN */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.60);
    z-index: 0;
}}

/* CONTENT ABOVE OVERLAY */
.main, .block-container {{
    position: relative;
    z-index: 1;
}}

/* TEXT */
h1, h2, h3, p, span, label {{
    color: white !important;
}}

/* INPUT */
input {{
    background-color: rgba(255,255,255,0.9) !important;
    color: black !important;
    border-radius: 10px !important;
}}

/* FORM */
div[data-testid="stForm"] {{
    border: 2px solid rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 18px;
    background: rgba(20, 20, 20, 0.4);
    backdrop-filter: blur(8px);
}}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {{
    background-image: url("data:image/jpg;base64,{sidebar_bg}");
    background-size: cover;
    background-position: center;
}}

/* SIDEBAR OVERLAY */
section[data-testid="stSidebar"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.55);
    z-index: 0;
}}

/* SIDEBAR CONTENT ABOVE OVERLAY */
section[data-testid="stSidebar"] > div {{
    position: relative;
    z-index: 1;
}}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {{
    color: white !important;
}}

/* SIDEBAR BUTTONS */
section[data-testid="stSidebar"] .stButton>button {{
    border: 2px solid white !important;
    border-radius: 8px;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# BACKEND CHECK
# =========================
try:
    # test = requests.get("http://127.0.0.1:8000/chat", params={"query": "test"})
    test = requests.get("https://pagan-wildcard-virtual.ngrok-free.dev/chat", params={"query": "test"})

    if test.status_code == 200:
        st.success("✅ Database connected | Backend running")
    else:
        st.error("❌ Backend issue detected")
except:
    st.error("❌ Unable to connect to backend")

# =========================
# HEADER
# =========================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 👨‍💼 AI Career Assistant")
    st.caption("Get job role suggestions based on your skills and experience")

with col2:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
        width=180
    )

# =========================
# SIDEBAR
# =========================
st.sidebar.header("About")
st.sidebar.info("AI RAG chatbot suggests job roles.")

st.sidebar.header("Settings")
top_k = st.sidebar.slider("Top K Results", 1, 5, 2)

st.sidebar.header("Tech Stack")

def tech_box(icon, name):
    return f"""
    <div style="
        border: 1px solid white;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        background-color: rgba(255,255,255,0.1);
    ">
        <img src="{icon}" width="30"/>
        <div style="font-size:13px; margin-top:5px;">{name}</div>
    </div>
    """

col1, col2 = st.sidebar.columns(2)

with col1:
    st.markdown(tech_box("https://cdn.simpleicons.org/fastapi", "FastAPI"), unsafe_allow_html=True)
    st.markdown(tech_box("https://cdn.simpleicons.org/apache", "FAISS"), unsafe_allow_html=True)
    st.markdown(tech_box("https://cdn.simpleicons.org/meta", "Ollama"), unsafe_allow_html=True)

with col2:
    st.markdown(tech_box("https://cdn.simpleicons.org/streamlit", "Streamlit"), unsafe_allow_html=True)
    st.markdown(tech_box("https://cdn.simpleicons.org/huggingface", "Sentence Transformers"), unsafe_allow_html=True)

st.sidebar.success("🧠 Indexed Knowledge Base: 29016")
st.sidebar.success("💻 Device Name: CPU")

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# INPUT FORM
# =========================
with st.form("chat_form"):
    user_input = st.text_input("Enter your query", key="input")
    ask = st.form_submit_button("🔍 Ask")
    clear = st.form_submit_button("🗑️ Clear")

if clear:
    st.session_state.messages = []
    st.rerun()

if ask and user_input:
    st.session_state.messages.append(("user", user_input))

    # res = requests.get("http://127.0.0.1:8000/chat", params={"query": user_input})
    res = requests.get("https://pagan-wildcard-virtual.ngrok-free.dev/chat", params={"query": user_input})


    if res.status_code == 200:
        reply = res.json()["response"]
        st.session_state.messages.append(("bot", reply))
    else:
        st.error("Backend error")

# =========================
# FORMAT RESPONSE
# =========================
def format_roles(text):
    roles = text.strip().split("\n\n")
    output = ""
    count = 1
    seen = set()

    for block in roles:
        lines = block.split("\n")
        if len(lines) < 3:
            continue

        role = lines[0].replace("Role:", "").strip()
        reason = lines[1].replace("Reason:", "").strip()
        skills = lines[2].replace("Skills:", "").strip()

        if not role or role in seen:
            continue

        seen.add(role)

        output += f"""
### 🎯 Suggested Role {count}: **{role}**

🧠 **Reason:**  
{reason}

🛠️ **Skills:**  
{skills}

---
"""
        count += 1

    return output

# =========================
# CHAT DISPLAY
# =========================
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown("🤖 **Bot:**")
        st.markdown(format_roles(msg))



















