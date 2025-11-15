import streamlit as st
import plotly.graph_objects as go
import random

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- Initialize session state ----
if "page" not in st.session_state:
    st.session_state.page = "Unity Hub"
if "map_points" not in st.session_state:
    st.session_state.map_points = []
if "submissions" not in st.session_state:
    st.session_state.submissions = []

# ---- Sidebar Navigation ----
if st.sidebar.button("Unity Hub"): st.session_state.page = "Unity Hub"
if st.sidebar.button("Language Lab"): st.session_state.page = "Language Lab"
if st.sidebar.button("Top Voices"): st.session_state.page = "Top Voices"
if st.sidebar.button("World of Words"): st.session_state.page = "World of Words"

# ---- Images ----
HOME_LOGO = "logo.png"
OTHER_HEADER = "header.jpg"

# ---- Sample translations and data ----
mock_translations = {
    "Break a leg": {"France":"Bonne chance","Germany":"Viel Glück","Spain":"Buena suerte"},
    "Why did the chicken cross the road?":{"France":"Pourquoi le poulet a traversé la route?","Germany":"Warum ging das Huhn über die Straße?","Spain":"Por qué cruzó el pollo la calle?"},
    "Knock knock": {"France":"Toc toc","Germany":"Klopf klopf","Spain":"Toc toc"}
}

country_coords = {
    "United States":[38,-97],
    "United Kingdom":[54,-2],
    "France":[46,2],
    "Germany":[51,10],
    "Spain":[40,-4],
    "Brazil":[-10,-55],
    "Japan":[36,138]
}

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

# ---------------- UNITY HUB ----------------
if st.session_state.page == "Unity Hub":
    st.image(HOME_LOGO, width=300)
    st.markdown("<h1 style='text-align:center;color:#1F77B4;font-size:60px;'>Welcome to <b>Unilang</b>! 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#FF7F0E;font-size:28px;'>Where languages and cultures unite!</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:20px;line-height:1.8;margin-bottom:20px;'>🚀 <b>Explore idioms and jokes from around the world</b><br>🗣️ <b>Learn how expressions are translated in different languages</b><br>🌟 <b>Discover the most popular phrases and share your favorites</b></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Centered Get Started Button
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        if st.button("🎯 Get Started!"):
            st.session_state.page = "Language Lab"
            st.experimental_rerun()  # ensures immediate navigation

    # Animated emoji
    st.markdown("""
    <style>
    @keyframes bounce {0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}
    .bounce {display:inline-block;animation:bounce 1s infinite;}
    </style>
    <p style='text-align:center;font-size:40px;'><span class='bounce'>🌐✨🎉</span></p>
    """, unsafe_allow_html=True)

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
            # --- Translation ---
            if user_text in mock_translations:
                translation = mock_translations[user_text].get(target_lang, user_text)
            else:
                # pseudo-translation: shuffle letters per word
                translation = " ".join(["".join(random.sample(word, len(word))) for word in user_text.split()])
            st.markdown(f"**Translation in {target_lang}:** {translation}")

            # --- Unity Meter ---
            unity_percent = random.randint(60, 100)
            st.progress(unity_percent)
            st.markdown(f"**Unity Meter:** {unity_percent}% resemblance")

            # --- Top 3 countries ---
            top3 = random.sample(list(country_coords.keys()), 3)
            st.markdown(f"**Top 3 countries with similar expression:** {', '.join(top3)}")

            # --- Store submission ---
            add_submission(user_text, choice_type, translation, unity_percent, top3)

# ---------------- WORLD OF WORDS ----------------
elif st.session_state.page == "World of Words":
    st.image(OTHER_HEADER, width=600)
    st.header("🗺️ World of Words")
    st.write("Explore idioms and jokes across countries!")

    # --- Filters ---
    filter_col, legend_col = st.columns([2,1])
    with filter_col:
        filter_type = st.radio("Filter by Type", ["All","Idiom","Joke"], horizontal=True)
    with legend_col:
        st.markdown("<p style='margin:0;'><span style='color:blue;'>● Idiom</span> &nbsp;&nbsp;<span style='color:orange;'>● Joke</span></p>", unsafe_allow_html=True)

    # --- Map ---
    lats, lons, colors, texts, sizes = [], [], [], [], []

    for sub in st.session_state.map_points:
        if filter_type=="All" or sub.get("type","Unknown")==filter_type:
            unity = sub.get("unity_percent", random.randint(60, 100))
            top3 = sub.get("top3", random.sample(list(country_coords.keys()),3))
            translation = sub.get("translation", sub.get("input","Unknown")[::-1])

            for country in sub.get("countries", []):
                if country in country_coords:
                    lat, lon = country_coords[country]
                    lats.append(lat)
                    lons.append(lon)
                    colors.append("blue" if sub.get("type","Idiom")=="Idiom" else "orange")
                    sizes.append(10 + unity/5)

                    # Hover with top3 in rectangle format
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

    # Top expressions
    st.subheader("🌟 Top Expressions")
    all_texts = [s.get("input","") for s in st.session_state.submissions]
    top_texts = {text:all_texts.count(text) for text in all_texts if text}
    top_sorted = sorted(top_texts.items(), key=lambda x:x[1], reverse=True)
    for text,count in top_sorted[:5]:
        st.markdown(f"- {text} ({count} submissions)")

    # Most humorous countries
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
