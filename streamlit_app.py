import streamlit as st
import pandas as pd
import random

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(page_title="UniLang", layout="wide")

# ----------------------------------
# LOAD CSV (English, French, German, Spanish)
# ----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("translations.csv")

translation_data = load_data()

# ----------------------------------
# TRANSLATION FUNCTION (Matches your CSV)
# ----------------------------------
def get_translation(text, lang):
    text = text.strip().lower()

    # Check English column ONLY
    row = translation_data[translation_data["English"].str.lower() == text]

    if not row.empty:
        return row[lang].iloc[0]   # lang is the actual column name (Spanish, French, German)

    return "No translation found in CSV."

# ----------------------------------
# PRELOADED ITEMS (do NOT depend on CSV)
# ----------------------------------
preloaded_items = [
    {"text": "Break the ice", "country": "USA", "type": "Idiom"},
    {"text": "Spill the tea", "country": "USA", "type": "Idiom"},
    {"text": "Not my circus, not my monkeys", "country": "Poland", "type": "Idiom"},
    {"text": "Why don’t eggs tell jokes? They’d crack each other up.", "country": "UK", "type": "Joke"},
    {"text": "I told my computer I needed a break, and it said 'No problem — I'll go to sleep.'", "country": "India", "type": "Joke"},
]

# ----------------------------------
# SESSION STATE
# ----------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "entries" not in st.session_state:
    st.session_state.entries = preloaded_items.copy()

# ----------------------------------
# NAVIGATION
# ----------------------------------
def go_to(page):
    st.session_state.page = page

# ----------------------------------
# SIDEBAR MENU
# ----------------------------------
with st.sidebar:
    st.title("🌍 UniLang Menu")
    st.button("Home", on_click=lambda: go_to("home"))
    st.button("Translator", on_click=lambda: go_to("translator"))
    st.button("Map", on_click=lambda: go_to("map"))
    st.button("Leaderboard", on_click=lambda: go_to("leaderboard"))

# ----------------------------------
# HOME PAGE
# ----------------------------------
if st.session_state.page == "home":
    st.markdown("<h1>🌍 UniLang</h1>", unsafe_allow_html=True)
    st.image("globe.png", width=250)

    if st.button("Get Started"):
        go_to("translator")

# ----------------------------------
# TRANSLATOR PAGE
# ----------------------------------
elif st.session_state.page == "translator":
    st.header("🔤 Translation Playground")

    user_text = st.text_input("Enter a phrase (must match CSV English column):")

    lang = st.selectbox(
        "Translate to:",
        ["Spanish", "French", "German"]
    )

    if st.button("Translate"):
        translation = get_translation(user_text, lang)
        st.success(f"**Translation:** {translation}")

        st.session_state.entries.append({
            "text": user_text,
            "country": random.choice(["USA", "France", "Spain", "Germany", "India"]),
            "type": "User"
        })

# ----------------------------------
# MAP PAGE (simple)
# ----------------------------------
elif st.session_state.page == "map":
    st.header("🗺️ Global Idioms & Jokes Map (Simple Demo)")
    df = pd.DataFrame(st.session_state.entries)
    st.dataframe(df, use_container_width=True)

# ----------------------------------
# LEADERBOARD
# ----------------------------------
elif st.session_state.page == "leaderboard":
    st.header("🏆 Leaderboard")

    df = pd.DataFrame(st.session_state.entries)

    leaderboard = (
        df["country"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Country", "country": "Count"})
    )

    st.dataframe(leaderboard, use_container_width=True)
