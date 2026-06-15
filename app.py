import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="LinguaAI Translator",
    page_icon="🌐",
    layout="wide"
)

# -----------------------------
# Load CSS
# -----------------------------

with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# -----------------------------
# Session State
# -----------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "translations_count" not in st.session_state:
    st.session_state.translations_count = 0

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "English"

if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Hindi"

# -----------------------------
# Languages
# -----------------------------

languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru",
    "Italian": "it",
    "Portuguese": "pt",
    "Turkish": "tr",
    "Dutch": "nl"
}

# -----------------------------
# Hero
# -----------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🌐 LinguaAI Translator</h1>
        <p>
            Translate across 15+ languages instantly
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Stats
# -----------------------------

c1, c2 = st.columns(2)

with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h2>{len(languages)}</h2>
            <p>Languages Supported</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <h2>{st.session_state.translations_count}</h2>
            <p>Total Translations</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# -----------------------------
# Language Selection
# -----------------------------

l1, l2, l3 = st.columns([5, 1, 5])

with l1:

    source_lang = st.selectbox(
        "Source Language",
        list(languages.keys()),
        index=list(languages.keys()).index(
            st.session_state.source_lang
        )
    )

with l2:

    st.write("")

    if st.button("🔄"):
        temp = st.session_state.source_lang
        st.session_state.source_lang = (
            st.session_state.target_lang
        )
        st.session_state.target_lang = temp
        st.rerun()

with l3:

    target_lang = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=list(languages.keys()).index(
            st.session_state.target_lang
        )
    )

st.session_state.source_lang = source_lang
st.session_state.target_lang = target_lang

# -----------------------------
# Input / Output
# -----------------------------

left, right = st.columns(2)

with left:

    text = st.text_area(
        "Input Text",
        height=300,
        placeholder="Type text here..."
    )

with right:

    st.text_area(
        "Translated Text",
        value=st.session_state.translated_text,
        height=300,
        disabled=True
    )

# -----------------------------
# Buttons
# -----------------------------

b1, b2 = st.columns(2)

with b1:

    translate = st.button(
        "🚀 Translate",
        use_container_width=True
    )

with b2:

    st.download_button(
        "⬇ Download Translation",
        st.session_state.translated_text,
        file_name="translation.txt",
        use_container_width=True
    )

# -----------------------------
# Translation
# -----------------------------

if translate:

    if text.strip() == "":

        st.warning(
            "Please enter text to translate."
        )

    elif source_lang == target_lang:

        st.warning(
            "Choose different languages."
        )

    else:

        try:

            translated_text = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(text)

            st.session_state.translated_text = (
                translated_text
            )

            st.session_state.translations_count += 1

            st.session_state.history.insert(
                0,
                {
                    "source": source_lang,
                    "target": target_lang,
                    "input": text,
                    "output": translated_text
                }
            )

            st.rerun()

        except Exception:

            st.error(
                "Translation failed. Check internet connection."
            )

# -----------------------------
# History
# -----------------------------

st.markdown("---")
st.subheader("📜 Translation History")

if not st.session_state.history:

    st.info("No translations yet.")

else:

    for item in st.session_state.history:

        with st.expander(
            f"{item['source']} → {item['target']}"
        ):

            st.write("**Input**")
            st.write(item["input"])

            st.write("**Output**")
            st.write(item["output"])

    st.write("")

    if st.button("🗑 Clear History"):

        st.session_state.history = []
        st.rerun()

        
# -----------------------------
# Footer
# -----------------------------

st.markdown(
    """
    <div class="footer">
        Built with ❤️ using Python, Streamlit and Google Translate
    </div>
    """,
    unsafe_allow_html=True
)