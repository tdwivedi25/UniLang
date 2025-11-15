import streamlit as st
import plotly.graph_objects as go
import random

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- SESSION STATE ----
if "page" not in st.session_state:
    st.session_state.page = "Unity Hub"

if "submissions" not in st.session_state:
    # Initialize sample submissions
    st.session_state.submissions = [
        {
            "input": "Break a leg",
            "literal": "Wish you luck",
            "type": "Idiom",
            "countries": ["United States","United Kingdom","Germany","France"],
            "top3": [
                ("France","Bonne chance"),
                ("Germany","Viel Glück"),
                ("Spain","Buena suerte")
            ]
        },
        {
            "input": "Why did the chicken cross the road?",
            "literal": "A classic joke",
            "type": "Joke",
            "countries": ["United States","Brazil","Japan"],
            "top3": [
                ("France","Pourquoi le poulet a traversé la route?"),
                ("Germany","Warum ging das Huhn über die Straße?"),
                ("Brazil","Por que a galinha atravessou a estrada?")
            ]
        },
    ]

# ---- SIDEBAR NAVIGATION ----
if st.sidebar.button("Unity Hub"): st.session_state.page = "Unity Hub"
if st.sidebar.button("Language Lab"): st.session_state.page = "Language Lab"
if st.sidebar.button("Top Voices"): st.session_state.page = "Top Voices"
if st.sidebar.button("World of Words"): st.session_state.page = "World of Words"

# ---- LOCAL IMAGES ----
home_header = "logo.png"       # Unity Hub
other_header = "header.jpg"    # Other pages

# ---- HANDLE HTML BUTTONS ----
query_params = st.experimental_get_query_params()
if query_params.get("page") == ["LanguageLab"]:
    st.session_state.page = "Language Lab"
    st.experimental_set_query_params()  # clear params

# ---------------------- UNITY HUB ----------------------
if st.session_state.page == "Unity Hub":
    # Centered Logo
    st.markdown(
        f"""
        <div style='text-align:center; margin-bottom:30px;'>
            <img src="{home_header}" style="width:300px;">
        </div>
        """, unsafe_allow_html=True
    )

    # Header text
    st.markdown("""
        <h1 style='text-align: center; color: #1F77B4; font-size: 60px;'>Welcome to <b>Unilang</b>! 🌍</h1>
        <h3 style='text-align: center; color: #FF7F0E; font-size: 28px;'>Where languages and cultures unite!</h3>
        <div style='text-align:center; font-size:20px; line-height:1.8; margin-bottom:20px;'>
        🚀 <b>Explore idioms and jokes from around the world</b><br>
        🗣️ <b>Learn how expressions are translated in different languages</b><br>
        🌟 <b>Discover the most popular phrases and share your favorites</b>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Get Started Button
    st.markdown("""
        <div style='text-align:center; margin:30px 0;'>
            <form action="?page=LanguageLab">
                <input type="submit" value="🎯 Get Started!" 
                style="background-color:#1F77B4; color:white; font-size:24px; padding:15px 40px; border:none; border-radius:12px; cursor:pointer;">
            </form>
        </div>
    """, unsafe_allow_html=True)

    # Animated emojis
    st.markdown("""
        <style>
        @keyframes bounce {0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}
        .bounce {display:inline-block; animation:bounce 1s infinite;}
        </style>
        <p style='text-align:center; font-size:40px;'><span class='bounce'>🌐✨🎉</span></p>
    """, unsafe_allow_html=True)

# ------------------- LANGUAGE LAB -------------------
elif st.session_state.page == "Language Lab":
    st.markdown(
        f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>",
        unsafe_allow_html=True
    )
    st.header("🔄 Language Lab")

    col1, col2 = st.columns([1,2])
    with col1:
        entry_type = st.selectbox("Select Type", ["Joke", "Idiom"])
        user_input = st.text_area(f"Enter your {entry_type}")
        target_country = st.selectbox("Translate to Country", ["France","Germany","Spain","Brazil","Japan","United States","United Kingdom"])

    with col2:
        if st.button("Translate"):
            if not user_input.strip():
                st.warning("Please enter something!")
            else:
                # Mock translation & unity score
                translation = f"{user_input[::-1]} ({target_country})"  # reversed for demo
                unity_score = random.randint(40, 99)
                similar_countries = random.sample(["France","Germany","Spain","Brazil","Japan","United States","United Kingdom"],3)

                # Save to map
                new_entry = {
                    "input": user_input,
                    "literal": "Auto-generated translation",
                    "type": entry_type,
                    "countries": similar_countries,
                    "top3": [(c, f"{user_input[::-1]}") for c in similar_countries]
                }
                st.session_state.submissions.append(new_entry)

                # Display results
                st.success(f"Translation: {translation}")
                st.info(f"Unity Meter: {unity_score}%")
                st.write("Top 3 countries with similar expression:")
                st.write(", ".join(similar_countries))

# ----------------------- WORLD OF WORDS -------------------------
elif st.session_state.page == "World of Words":
    st.markdown(
        f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>",
        unsafe_allow_html=True
    )
    st.header("🗺️ World of Words")
    st.write("Filter and explore idioms & jokes across countries!")

    filter_col, legend_col = st.columns([2,1])
    with filter_col:
        filter_type = st.radio("Filter by Type", ["All", "Idiom", "Joke"], horizontal=True)
    with legend_col:
        st.markdown("<p style='margin:0;'><span style='color:blue;'>● Idiom</span> &nbsp;&nbsp; <span style='color:orange;'>● Joke</span></p>", unsafe_allow_html=True)

    lats, lons, colors, texts = [], [], [], []
    country_coords = {"United States":[38,-97],"United Kingdom":[54,-2],"France":[46,2],"Germany":[51,10],"Spain":[40,-4],"Brazil":[-10,-55],"Japan":[36,138]}

    for sub in st.session_state.submissions:
        if "type" not in sub or (filter_type!="All" and sub["type"]!=filter_type): continue
        for c in sub.get("countries", []):
            if c not in country_coords: continue
            lat, lon = country_coords[c]
            lats.append(lat)
            lons.append(lon)
            colors.append("blue" if sub.get("type")=="Idiom" else "orange")
            top3_bullets = "<br>   - ".join([f"{c2}: {t}" for c2,t in sub.get("top3",[])])
            texts.append(f"<b>{sub.get('input','')}</b><br>• Literal: {sub.get('literal','')}<br>• Similar: {top3_bullets}")

    if not lats:
        st.info("No entries to display for this filter.")
    else:
        fig = go.Figure(go.Scattergeo(
            lon=lons, lat=lats, text=texts, mode='markers',
            marker=dict(size=35, color=colors, line=dict(width=1, color='black')), hoverinfo='text'
        ))
        fig.update_layout(
            geo=dict(showland=True, landcolor="rgb(200,230,201)", showcountries=True, countrycolor="rgb(100,100,100)", projection_type='natural earth'),
            margin={"r":0,"t":0,"l":0,"b":0}, height=800
        )
        st.plotly_chart(fig, use_container_width=True)

# ------------------- TOP VOICES / LEADERSHIP -------------------
elif st.session_state.page == "Top Voices":
    st.markdown(
        f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>",
        unsafe_allow_html=True
    )
    st.header("🏆 Leadership Dashboard")

    # Top jokes/idioms
    st.subheader("Top Expressions Worldwide")
    top_expressions = sorted(st.session_state.submissions, key=lambda x: random.random(), reverse=True)[:5]
    for i, expr in enumerate(top_expressions,1):
        st.write(f"{i}. ({expr.get('type','')}) {expr.get('input','')}")

    # Bar chart: most humorous country
    country_counts = {}
    for sub in st.session_state.submissions:
        for c in sub.get("countries", []):
            country_counts[c] = country_counts.get(c,0)+1

    if country_counts:
        countries = list(country_counts.keys())
        values = [random.randint(1,10) for _ in countries]  # varied heights
        fig = go.Figure(go.Bar(x=countries, y=values, marker_color='orange'))
        fig.update_layout(title="Most Humorous Countries", xaxis_title="Country", yaxis_title="Score")
        st.plotly_chart(fig, use_container_width=True)
