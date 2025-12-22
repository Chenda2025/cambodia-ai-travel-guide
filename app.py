import streamlit as st
from core.translations import languages
import requests

# Load Custom CSS
with open("static/css/custom.css", "r", encoding="utf-8") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Page Config
st.set_page_config(
    page_title="Cambodia AI Travel Guide",
    page_icon="🇰🇭",
    layout="wide"
)

# Hero Header
st.markdown("""
<div class="hero-header">
    <h1 style="font-size:4.5rem; margin:0;">🇰🇭 Cambodia AI Travel Guide</h1>
    <p style="font-size:2rem; margin:15px 0;">Your Smart Companion to the Kingdom of Wonders</p>
</div>
""", unsafe_allow_html=True)

# === BEST SIDEBAR DESIGN ===
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h2 style="color: #d35400; margin:0;">🇰🇭 Cambodia Guide</h2>
    <p style="color: #e67e22; font-weight: bold; margin:5px 0;">AI Travel Assistant</p>
    <hr style="border-color: #e67e22; width: 80%;">
</div>
""", unsafe_allow_html=True)

# Language Selector
st.sidebar.markdown("### 🌐 Language / ភាសា")
selected_lang_name = st.sidebar.selectbox(
    "Select Language",
    options=list(languages.keys()),
    index=0,
    label_visibility="collapsed"
)
lang = languages[selected_lang_name]

# Navigation
st.sidebar.markdown("### 📍 " + lang["navigation"])

pages = [
    (lang["home"], "🏠"),
    (lang["attractions"], "🏛️"),
    (lang["food"], "🍲"),
    (lang["tips"], "💡"),
    (lang["ai"], "🤖")
]

page_labels = [f"{icon} {name}" for name, icon in pages]
page_keys = [name for name, _ in pages]

selected_page_label = st.sidebar.radio(
    lang["navigation"],
    page_labels,
    label_visibility="collapsed"
)

page_map = dict(zip(page_labels, page_keys))
page = page_map[selected_page_label]

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 by Tob Chenda | BELTIE International School")
st.sidebar.caption("Powered by Streamlit")

# ==================== PAGES ====================

if page == lang["home"]:
    st.markdown(f"<h2 style='text-align:center;'>{lang['discover']}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("static/images/koh_rong.jpg", caption="Koh Rong Paradise" if selected_lang_name == "English" else "កោះរ៉ុងសួគ៌", width=None)
    with col2:
        st.image("static/images/amok.jpg", caption="Delicious Fish Amok" if selected_lang_name == "English" else "អាម៉ុកត្រីឆ្ងាញ់", width=None)
    st.info(lang["welcome"])

elif page == lang["attractions"]:
    st.markdown(f"<h2 style='text-align:center;'>{lang['must_visit']}</h2>", unsafe_allow_html=True)
    
    attractions = [
        ("Angkor Wat", "World's largest religious monument – UNESCO World Heritage", "static/images/angkor_wat.jpg", "Siem Reap"),
        ("Bayon Temple", "Famous for 216 giant smiling stone faces", "static/images/bayon.jpg", "Angkor Thom"),
        ("Royal Palace", "Stunning golden Khmer architecture and Silver Pagoda", "static/images/royal_palace.jpg", "Phnom Penh")
    ]
    
    for name, desc, img_path, location in attractions:
        st.image(img_path, width=None)
        st.markdown(f"<h3 style='text-align:center; color:#d35400;'>{name} — {location}</h3>", unsafe_allow_html=True)
        st.write(desc)
        st.divider()

elif page == lang["food"]:
    st.markdown(f"<h2 style='text-align:center;'>{lang['cuisine']}</h2>", unsafe_allow_html=True)
    st.write(lang["cuisine_desc"])

elif page == lang["tips"]:
    st.markdown(f"<h2 style='text-align:center;'>{lang['essential_tips']}</h2>", unsafe_allow_html=True)
    st.markdown("""
    - **Best time to visit**: November – February (cool & dry)  
    - **Visa**: e-Visa online ($36) or visa on arrival  
    - **Currency**: US Dollars widely accepted  
    - **Transport**: Tuk-tuk, Grab, PassApp  
    - **Temples**: Cover shoulders and knees  
    """)

elif page == lang["ai"]:
    st.markdown(f"<h2 style='text-align:center;'>{lang['ask_ai']}</h2>", unsafe_allow_html=True)
    st.write(lang["ask_prompt"])

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble">{message["content"]}</div>', unsafe_allow_html=True)

    # User input
    user_input = st.text_input(
        "Your question",
        placeholder=lang["input_placeholder"],
        key="user_input",
        label_visibility="collapsed"
    )

    if st.button(lang["get_answer"]):
        if user_input.strip():
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})

            # ====== REAL GROK AI INTEGRATION ======
            API_KEY = "YOUR_GROK_API_KEY_HERE"  # ← REPLACE with your key from https://x.ai/api

            url = "https://api.x.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            # Expert Cambodia travel system prompt
            system_prompt = """
            You are an expert Cambodia travel guide. 
            Answer in the same language as the user (English or Khmer).
            Be friendly, helpful, detailed, and use emojis.
            Cover attractions, food, transport, visa, budget, safety, culture.
            Make personalized recommendations.
            """

            messages = [
                {"role": "system", "content": system_prompt}
            ]

            # Add chat history
            for msg in st.session_state.messages[:-1]:
                messages.append({"role": msg["role"], "content": msg["content"]})

            # Add current user message
            messages.append({"role": "user", "content": user_input})

            data = {
                "model": "grok-beta",
                "messages": messages,
                "temperature": 0.8,
                "max_tokens": 1000
            }

            with st.spinner("Grok is thinking... 🤖"):
                try:
                    response = requests.post(url, headers=headers, json=data, timeout=30)
                    if response.status_code == 200:
                        result = response.json()
                        ai_response = result["choices"][0]["message"]["content"]
                    else:
                        ai_response = f"API error {response.status_code}: {response.text}"
                except Exception as e:
                    ai_response = f"Connection error: {str(e)}. Check internet or API key."

            # Add AI response
            st.session_state.messages.append({"role": "ai", "content": ai_response})
            st.rerun()

# Footer
st.markdown("---")
st.caption(lang["footer"])