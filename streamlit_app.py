import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random

# ---- APP CONFIG ----
st.set_page_config(page_title="UniLang", page_icon="🌍", layout="wide")

# ---- Initialize session state ----
if "page" not in st.session_state:
    st.session_state.page = "Unity Hub"
if "map_points" not in st.session_state:
    st.session_state.map_points = []
if "submissions" not in st.session_state:
    st.session_state.submissions = []
if "start_clicked" not in st.session_state:
    st.session_state.start_clicked = False

# ---- Sidebar Navigation ----
if st.sidebar.button("Unity Hub"): st.session_state.page = "Unity Hub"
if st.sidebar.button("Language Lab"): st.session_state.page = "Language Lab"
if st.sidebar.button("Top Voices"): st.session_state.page = "Top Voices"
if st.sidebar.button("World of Words"): st.session_state.page = "World of Words"

# ---- Images ----
HOME_LOGO = "globe.png"
OTHER_HEADER = "header.jpg"

# ---- Country coordinates ----
country_coords = {
    "United States":[38,-97],
    "United Kingdom":[54,-2],
    "France":[46,2],
    "Germany":[51,10],
    "Spain":[40,-4],
    "Brazil":[-10,-55],
    "Japan":[36,138]
}

# ---- Load CSV dataset ----
# CSV should have columns: 'text', 'type', 'France', 'Germany', 'Spain'
translations_df = pd.read_csv("translations.csv")

# ---- Helper to get translation ----
def get_translation(user_text, target_lang):
    row = translations_df[translations_df["text"].str.lower() == user_text.lower()]
    if not row.empty:
        return row.iloc[0][target_lang]
    else:
        # fallback: shuffle letters per word
        return " ".join(["".join(random.sample(word, len(word))) for word in user_text.split()])

# ---- Helper to add submission ----
def add_submission(text, typ, translation, unity_percent, top3):
    data = {
        "input": text,
        "type": typ,
        "countries": list(country_coords.keys()),
        "translation": translation,
        "unity_percent": unity_percent,
        "top3": top3
    }
    st.session_state.submissions.append(data)
    st.session_state.map_points.append(data)

# ---- Preload 5 idioms and 5 jokes ----
preloaded = [
    {"text":"Break a leg","type":"Idiom"},
    {"text":"Knock on wood","type":"Idiom"},
    {"text":"Piece of cake","type":"Idiom"},
    {"text":"Raining cats and dogs","type":"Idiom"},
    {"text":"Spill the beans","type":"Idiom"},
    {"text":"Why did the chicken cross the road?","type":"Joke"},
    {"text":"Knock knock","type":"Joke"},
    {"text":"I told my computer I needed a break, it said 'No problem, I'll go to sleep'","type":"Joke"},
    {"text":"Why don’t scientists trust atoms? Because they make up everything!","type":"Joke"},
    {"text":"Parallel lines have so much in common. It’s a shame they’ll never meet.","type":"Joke"}
]

for item in preloaded:
    user_text = item["text"]
    choice_type = item["type"]
    target_lang = random.choice(["France","Germany","Spain"])
    translation = get_translation(user_text, target_lang)
    unity_percent = random.randint(70,100)
    top3 = random.sample(list(country_coords.keys()),3)
    add_submission(user_text, choice_type, translation, unity_percent, top3)

# ---------------- UNITY HUB ----------------
if st.session_state.page == "Unity Hub":
    st.image(HOME_LOGO, width=300)
    st.markdown("<h1 style='text-align:left;color:#1F77B4;font-size:60px;'>Welcome to <b>UniLang</b>! 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:left;color:#FF7F0E;font-size:28px;'>Where languages and cultures unite!</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:left;font-size:20px;line-height:1.8;margin-bottom:20px;'>🚀 <b>Explore idioms and jokes from around the world</b><br>🗣️ <b>Learn how expressions are translated in different languages</b><br>🌟 <b>Discover the most popular phrases and share your favorites</b></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Centered Get Started Button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🎯 Get Started!"):
            st.session_state.page = "Language Lab"

# ---------------- LANGUAGE LAB ----------------
elif st.session_state.page == "Language Lab":
    st.image(OTHER_HEADER, width=600)
    st.header("🔄 Language Lab")
    st.write("Enter an idiom or joke to see its translation, similarity, and Unity Meter.")

    col_type, col_input, col_lang = st.columns([1,2,1])
    with col_type:
        choice_type = st.selectbox("Select Type", ["Idiom", "Joke"])
    with col_input:
        user_text = st.text_input("Enter text:")
    with col_lang:
        target_lang = st.selectbox("Translate to", ["France","Germany","Spain"])

    if st.button("Translate!"):
        if user_text.strip() == "":
            st.warning("Please enter some text!")
        else:
            translation = get_translation(user_text, target_lang)
            unity_percent = random.randint(60, 100)
            top3 = random.sample(list(country_coords.keys()), 3)
            st.markdown(f"**Translation in {target_lang}:** {translation}")
            st.progress(unity_percent)
            st.markdown(f"**Unity Meter:** {unity_percent}% resemblance")
            st.markdown(f"**Top 3 countries with similar expression:** {', '.join(top3)}")
            add_submission(user_text, choice_type, translation, unity_percent, top3)

# ---------------- WORLD OF WORDS ----------------
elif st.session_state.page == "World of Words":
    st.image(OTHER_HEADER, width=600)
    st.header("🗺️ World of Words")
    st.write("Explore idioms and jokes across countries!")

    filter_col, legend_col = st.columns([2,1])
    with filter_col:
        filter_type = st.radio("Filter by Type", ["All","Idiom","Joke"], horizontal=True)
    with legend_col:
        st.markdown("<p style='margin:0;'><span style='color:blue;'>● Idiom</span> &nbsp;&nbsp;<span style='color:orange;'>● Joke</span></p>", unsafe_allow_html=True)

    lats, lons, colors, texts, sizes = [], [], [], [], []

    # ---- FIXED: show both types when "All" is selected ----
    for sub in st.session_state.map_points:
        if filter_type=="All" or sub.get("type","Unknown")==filter_type:
            unity = sub.get("unity_percent", random.randint(60, 100))
            top3 = sub.get("top3", random.sample(list(country_coords.keys()),3))
            translation = sub.get("translation", sub.get("input","Unknown"))

            for country in sub.get("countries", []):
                if country in country_coords:
                    lat, lon = country_coords[country]
                    lats.append(lat)
                    lons.append(lon)
                    colors.append("blue" if sub.get("type","Idiom")=="Idiom" else "orange")
                    sizes.append(10 + unity/5)
                    top3_html = "<br>".join([f"&#9632; {c}" for c in top3])
                    hover_text = (
                        f"<b>{sub.get('input','Unknown')} ({sub.get('type','Unknown')})</b><br>"
                        f"<b>Translation:</b> {translation}<br>"
                        f"<b>Unity Meter:</b> {unity}%<br>"
                        f"<b>Top 3 Similar Countries:</b><br>{top3_html}"
                    )
                    texts.append(hover_text)

    fig = go.Figure(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=texts,
        mode='markers',
        marker=dict(size=sizes, color=colors, line=dict(width=1,color='black')),
        hoverinfo='text'
    ))
    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="rgb(200,230,201)",
            showcountries=True,
            countrycolor="rgb(100,100,100)",
            projection_type='natural earth'
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=1000
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TOP VOICES ----------------
elif st.session_state.page == "Top Voices":
    st.image(OTHER_HEADER, width=600)
    st.header("🏆 Leadership Dashboard")

    st.subheader("🌟 Top Expressions")
    all_texts = [s.get("input","") for s in st.session_state.submissions]
    top_texts = {text:all_texts.count(text) for text in all_texts if text}
    top_sorted = sorted(top_texts.items(), key=lambda x:x[1], reverse=True)
    for text,count in top_sorted[:5]:
        st.markdown(f"- {text} ({count} submissions)")

    country_counts = {c:0 for c in country_coords.keys()}
    for sub in st.session_state.submissions:
        for c in sub.get("countries",[]):
            country_counts[c]+=1
    countries = list(country_counts.keys())
    counts = [country_counts[c]+random.randint(0,5) for c in countries]
    st.subheader("😂 Most Humorous Countries")
    fig_bar = go.Figure([go.Bar(x=countries,y=counts,marker_color='orange')])
    fig_bar.update_layout(yaxis_title="Submissions", xaxis_title="Country", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)
