import streamlit as st
import pandas as pd
import random

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="UniLang", layout="wide")

# ---------------------------------------------------
# LOAD CSV DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("translations.csv")   # MUST contain: input, language, translation

translation_data = load_data()

# ---------------------------------------------------
# PRELOADED IDIOMS + JOKES
# ---------------------------------------------------
preloaded_items = [
    {"text": "Break the ice", "country": "USA", "type": "Idiom"},
    {"text": "Spill the tea", "country": "USA", "type": "Idiom"},
    {"text": "Not my circus, not my monkeys", "country": "Poland", "type": "Idiom"},
    {"text": "Why don’t eggs tell jokes? They’d crack each other up.", "country": "UK", "type": "Joke"},
    {"text": "I told my computer I needed a break, and it said 'No problem — I'll go to sleep.'", "country": "India", "type": "Joke"},
]

# ---------------------------------------------------
# TRANSLATION FUNCTION (dataset-based)
# ---------------------------------------------------
def get_translation(text, lang):
    text = text.strip().lower()
    lang = lang.strip().lower()

    row = translation_data[
        (translation_data["input"].str.lower() == text) &
        (translation_data["language"].str.lower() == lang)
    ]

    if not row.empty:
        return row["translation"].iloc[0]
    return "No translation found."

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "entries" not in st.session_state:
    st.session_state.entries = preloaded_items.copy()

# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------
st.sidebar.title("🌍 UniLang Menu")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Translator", "Map", "Leaderboard"]
)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "Home":
    st.markdown("<h1 style='text-align:left;'>🌍 UniLang</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:left;font-size:18px;'>Explore cultural idioms, jokes, and translations in a fun way!</p>",
        unsafe_allow_html=True
    )

    st.image("globe.png", width=300)

    st.info("Use the sidebar to get started!")

# ---------------------------------------------------
# TRANSLATOR PAGE
# ---------------------------------------------------
elif page == "Translator":

    st.markdown("## 🔤 Translation Playground")

    user_text = st.text_input("Enter a phrase to translate:")

    lang = st.selectbox("Translate to:", ["Spanish", "French", "German", "Hindi", "Korean"])

    if st.button("Translate"):
        translation = get_translation(user_text, lang)
        st.success(f"**Translation:** {translation}")

        # Save entry for map + leaderboard
        if user_text.strip():
            st.session_state.entries.append({
                "text": user_text,
                "country": random.choice(["USA", "France", "Spain", "Germany", "India", "Korea"]),
                "type": "User"
            })

# ---------------------------------------------------
# MAP PAGE (simple table version)
# ---------------------------------------------------
elif page == "Map":
    st.markdown("## 🗺️ Global Idioms & Jokes Map")

    df = pd.DataFrame(st.session_state.entries)

    st.dataframe(df, use_container_width=True)

# ---------------------------------------------------
# LEADERBOARD PAGE
# ---------------------------------------------------
elif page == "Leaderboard":
    st.markdown("## 🏆 Leaderboard (Most Cultural Items Added)")

    df = pd.DataFrame(st.session_state.entries)

    leaderboard = (
        df["country"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Country", "country": "Count"})
    )

    st.dataframe(leaderboard, use_container_width=True)
