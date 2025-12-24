import streamlit as st
import requests
import time
from core.translations import languages

# Load Custom CSS
try:
    with open("static/css/custom.css", "r", encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("CSS file not found — using default styling.")

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

# === SIDEBAR ===
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #fbbf24; margin:0;">🇰🇭 Cambodia Guide</h2>
        <p style="color: #fcd34d; font-weight: bold; margin:5px 0;">AI Travel Assistant</p>
        <hr style="border-color: #334155; width: 80%;">
    </div>
    """, unsafe_allow_html=True)

    # Language Selector
    st.markdown("### 🌐 Language / ភាសា")
    flag_map = {"English": "🇬🇧", "Khmer": "🇰🇭"}
    cols = st.columns(len(languages))
    selected_lang_name = st.session_state.get("selected_lang_name", list(languages.keys())[0])
    for col, lang_name in zip(cols, languages.keys()):
        flag = flag_map.get(lang_name, "🌍")
        if col.button(
            f"{flag} {lang_name}",
            width="stretch",  # Fixed
            key=f"lang_{lang_name}",
            type="primary" if selected_lang_name == lang_name else "secondary"
        ):
            selected_lang_name = lang_name
            st.session_state.selected_lang_name = selected_lang_name
            st.rerun()
    lang = languages[selected_lang_name]
    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation
    st.markdown("### 📍 " + lang["navigation"])
    pages = [
        (lang["home"], "🏠"),
        (lang["attractions"], "🏛️"),
        (lang["food"], "🍲"),
        (lang["tips"], "💡"),
        (lang["ai"], "🤖")
    ]
    page_labels = [f"{icon} {name}" for name, icon in pages]
    selected_page_label = st.radio(
        lang["navigation"],
        page_labels,
        label_visibility="collapsed",
        key="nav_radio"
    )
    page_map = dict(zip(page_labels, [name for name, _ in pages]))
    page = page_map[selected_page_label]

    st.markdown("---")
    st.caption("© 2025 by Tob Chenda | BELTIE International School")
    st.caption("Powered by Streamlit")

# === PAGE CONTENT ===
if page == lang["home"]:
    st.markdown(f"<h2 style='text-align:center;'>{lang['discover']}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("static/images/koh_rong.jpg", caption="Koh Rong Paradise" if selected_lang_name == "English" else "កោះរ៉ុងសួគ៌", use_container_width=True)
    with col2:
        st.image("static/images/amok.jpg", caption="Delicious Fish Amok" if selected_lang_name == "English" else "អាម៉ុកត្រីឆ្ងាញ់", use_container_width=True)
    st.info(lang["welcome"])

elif page == lang["attractions"]:
    st.markdown(f"<h2 style='text-align:center;'>{lang['must_visit']}</h2>", unsafe_allow_html=True)
    attractions = [
        ("Angkor Wat", "World's largest religious monument – UNESCO World Heritage", "static/images/angkor_wat.jpg", "Siem Reap"),
        ("Bayon Temple", "Famous for 216 giant smiling stone faces", "static/images/bayon.jpg", "Angkor Thom"),
        ("Royal Palace", "Stunning golden Khmer architecture and Silver Pagoda", "static/images/royal_palace.jpg", "Phnom Penh")
    ]
    for name, desc, img_path, location in attractions:
        st.image(img_path, use_container_width=True)
        st.markdown(f"<h3 style='text-align:center; color:#fbbf24;'>{name} — {location}</h3>", unsafe_allow_html=True)
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
    st.markdown(f"<h2 style='text-align:center; color:#fbbf24; margin-bottom: 1rem;'>{lang['ask_ai']}</h2>", unsafe_allow_html=True)
    st.write(lang["ask_prompt"])

    # Initialize guest chat history
    if "guest_messages" not in st.session_state:
        st.session_state.guest_messages = []

    messages = st.session_state.guest_messages

    # Beautiful welcome message
    if not messages:
        welcome_msg = """
        🇰🇭 **សួស្តី! Hello and welcome!**  
        
        I'm your personal **Cambodia AI Travel Guide** — here to help you discover the Kingdom of Wonders! 🌟
        
        Ask me anything:
        - Best temples & hidden gems in Siem Reap
        - Beach paradise on Koh Rong or Koh Rong Samloem
        - Must-try Khmer food & street eats
        - Visa, budget, transport tips
        - Itinerary ideas for 3–7 days
        - Safety, culture, and local secrets
        
        Let's plan your dream trip together! 😊✨
        """
        messages.append({"role": "assistant", "content": welcome_msg})

    # Chat container with auto-scroll
    chat_container = st.container()

    with chat_container:
        for message in messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🇰🇭"):
                    st.markdown(message["content"])

    # Chat input at bottom
    user_input = st.chat_input(
        placeholder=lang.get("input_placeholder", "Ask me anything about Cambodia... 🌴"),
        key="chat_input"
    )

    if user_input and user_input.strip():
        # Add user message
        messages.append({"role": "user", "content": user_input.strip()})

        # Rate limit check
        current_time = time.time()
        if "last_request_time" not in st.session_state:
            st.session_state.last_request_time = 0
        if current_time - st.session_state.last_request_time < 5:
            st.warning("⏳ Please wait 5 seconds between questions to keep the magic flowing! 😊")
            messages.pop()  # remove the rushed message
            st.rerun()

        st.session_state.last_request_time = current_time

        # Show thinking spinner + AI response
        with st.chat_message("assistant", avatar="🇰🇭"):
            with st.spinner("🧠 Thinking about the best Cambodia tips for you..."):
                try:
                    API_KEY = st.secrets["OPENAI_API_KEY"]
                    url = "https://api.openai.com/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    }
                    system_prompt = """
                    You are an expert Cambodia travel guide.
                    Answer in the same language as the user (English or Khmer).
                    Be friendly, helpful, detailed, and use lots of emojis.
                    Cover attractions, food, transport, visa, budget, safety, culture.
                    Make personalized recommendations.
                    """
                    api_messages = [{"role": "system", "content": system_prompt}]
                    for msg in messages[:-1]:
                        api_messages.append({"role": msg["role"], "content": msg["content"]})
                    api_messages.append({"role": "user", "content": user_input.strip()})

                    data = {
                        "model": "gpt-4o-mini",
                        "temperature": 0.8,
                        "max_tokens": 1000,
                        "messages": api_messages
                    }

                    response = requests.post(url, headers=headers, json=data, timeout=30)
                    if response.status_code == 200:
                        ai_response = response.json()["choices"][0]["message"]["content"]
                    else:
                        ai_response = "😔 Sorry, I'm having a little trouble right now. Please try again in a moment!"
                except Exception:
                    ai_response = "🌐 Connection issue — please check your internet and try again!"

            st.markdown(ai_response)

        # Add AI response to history
        messages.append({"role": "assistant", "content": ai_response})

        # Force rerun to update chat
        st.rerun()

    # === AUTO-SCROLL TO BOTTOM (smooth & perfect) ===
    st.components.v1.html(
        """
        <script>
        const main = parent.document.querySelector('section.main');
        if (main) {
            main.scrollTo({
                top: main.scrollHeight,
                behavior: 'smooth'
            });
        }
        </script>
        """,
        height=0
    )

# Footer
st.markdown("---")
st.caption(lang["footer"])