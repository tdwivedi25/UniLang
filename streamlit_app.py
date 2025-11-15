import streamlit as st
import plotly.graph_objects as go
import random

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- SESSION STATE ----
if "page" not in st.session_state:
    st.session_state.page = "Unity Hub"
if "submissions" not in st.session_state:
    st.session_state.submissions = [
        # Pre-populated examples
        {
            "input": "Break a leg",
            "type": "Idiom",
            "language": "English",
            "translations": {"French": "Bonne chance", "German": "Viel Glück", "Spanish": "Buena suerte"},
            "countries": ["France","Germany","Spain"],
            "points": 1
        },
        {
            "input": "Why did the chicken cross the road?",
            "type": "Joke",
            "language": "English",
            "translations": {"French": "Pourquoi le poulet a traversé la route?", "German": "Warum ging das Huhn über die Straße?", "Brazil": "Por que a galinha atravessou a estrada?"},
            "countries": ["France","Germany","Brazil"],
            "points": 1
        }
    ]

# ---- SIDEBAR NAVIGATION ----
if st.sidebar.button("Unity Hub"):
    st.session_state.page = "Unity Hub"
if st.sidebar.button("Language Lab"):
    st.session_state.page = "Language Lab"
if st.sidebar.button("Top Voices"):
    st.session_state.page = "Top Voices"
if st.sidebar.button("World of Words"):
    st.session_state.page = "World of Words"

# ---- LOCAL IMAGES ----
home_header = "logo.png"
other_header = "header.jpg"

# ---------------------- UNITY HUB ----------------------
if st.session_state.page == "Unity Hub":
    st.markdown(f"<div style='text-align:center; margin-bottom:30px;'><img src='{home_header}' style='width:300px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#1F77B4; font-size:60px;'>Welcome to <b>Unilang</b>! 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#FF7F0E; font-size:28px;'>Where languages and cultures unite!</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:20px; line-height:1.8; margin-bottom:20px;'>🚀 <b>Explore idioms and jokes from around the world</b><br>🗣️ <b>Learn how expressions are translated in different languages</b><br>🌟 <b>Discover the most popular phrases and share your favorites</b></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Get Started Button (working)
    st.markdown("""
        <div style='text-align:center; margin:30px 0;'>
            <a href='?page=LanguageLab'>
                <button style='background-color:#1F77B4; color:white; font-size:24px; padding:15px 40px; border:none; border-radius:12px; cursor:pointer;'>🎯 Get Started!</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

    # Animated Emoji
    st.markdown("""
        <style>
        @keyframes bounce {0%,100% {transform:translateY(0);}50%{transform:translateY(-10px);}}
        .bounce {display:inline-block; animation:bounce 1s infinite;}
        </style>
        <p style='text-align:center; font-size:40px;'><span class='bounce'>🌐✨🎉</span></p>
    """, unsafe_allow_html=True)

# ------------------- LANGUAGE LAB -------------------
elif st.session_state.page == "Language Lab":
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>", unsafe_allow_html=True)
    st.header("🔄 Language Lab")
    
    st.markdown("**Select Type and Input an Expression:**")
    expr_type = st.selectbox("Type:", ["Idiom", "Joke"])
    expr_input = st.text_input("Enter your idiom or joke (any language):")
    target_lang = st.selectbox("Translate to:", ["English", "French", "German", "Spanish", "Brazilian Portuguese"])
    
    if st.button("Translate"):
        if expr_input:
            # Simulate translation
            translation = expr_input[::-1]  # placeholder for non-literal translation
            top3_countries = random.sample(["France","Germany","Spain","Brazil","Japan","United States"], 3)
            unity_percent = random.randint(60,100)
            
            st.success(f"**Translation ({target_lang}):** {translation}")
            st.info(f"**Unity Meter:** {unity_percent}%")
            st.write(f"**Top 3 Countries with Similar Expression:** {', '.join(top3_countries)}")
            
            # Save submission
            st.session_state.submissions.append({
                "input": expr_input,
                "type": expr_type,
                "language": target_lang,
                "translations": {target_lang: translation},
                "countries": top3_countries,
                "points": 1
            })
        else:
            st.warning("Please enter an expression!")

# -------------------- TOP VOICES / LEADERSHIP DASHBOARD --------------------
elif st.session_state.page == "Top Voices":
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>", unsafe_allow_html=True)
    st.header("🏆 Leadership Dashboard")
    
    # Top Jokes/Idioms Leaderboard
    st.subheader("🔥 Top Jokes & Idioms")
    sorted_subs = sorted(st.session_state.submissions, key=lambda x: x["points"], reverse=True)[:10]
    for i, sub in enumerate(sorted_subs, start=1):
        st.write(f"{i}. ({sub['type']}) {sub['input']} – {sub['points']} points – Countries: {', '.join(sub['countries'])}")
    
    # Bar chart: most humorous country
    country_points = {}
    for sub in st.session_state.submissions:
        for country in sub["countries"]:
            country_points[country] = country_points.get(country, 0) + sub["points"]
    
    fig = go.Figure(go.Bar(
        x=list(country_points.keys()),
        y=list(country_points.values()),
        marker_color=[f'rgb({random.randint(50,255)},{random.randint(50,255)},{random.randint(50,255)})' for _ in country_points]
    ))
    fig.update_layout(title="Most Humorous Countries", yaxis_title="Points", xaxis_title="Country")
    st.plotly_chart(fig, use_container_width=True)

# ----------------------- WORLD OF WORDS -------------------------
elif st.session_state.page == "World of Words":
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>", unsafe_allow_html=True)
    st.header("🗺️ World of Words")
    
    filter_col, legend_col = st.columns([2,1])
    with filter_col:
        filter_type = st.radio("Filter by Type", ["All", "Idiom", "Joke"], horizontal=True)
    with legend_col:
        st.markdown("<p style='margin:0;'><span style='color:blue;'>● Idiom</span> &nbsp;&nbsp;<span style='color:orange;'>● Joke</span></p>", unsafe_allow_html=True)
    
    # Plot map
    lats, lons, colors, texts = [], [], [], []
    country_coords = {
        "United States":[38,-97],
        "United Kingdom":[54,-2],
        "France":[46,2],
        "Germany":[51,10],
        "Spain":[40,-4],
        "Brazil":[-10,-55],
        "Japan":[36,138]
    }
    
    filtered_subs = [s for s in st.session_state.submissions if filter_type=="All" or s["type"]==filter_type]
    
    for sub in filtered_subs:
        for country in sub["countries"]:
            if country in country_coords:
                lat, lon = country_coords[country]
                lats.append(lat)
                lons.append(lon)
                colors.append("blue" if sub["type"]=="Idiom" else "orange")
                hover_text = f"<b>{sub['input']}</b><br>Type: {sub['type']}<br>Countries: {', '.join(sub['countries'])}"
                texts.append(hover_text)
    
    fig = go.Figure(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=texts,
        mode='markers',
        marker=dict(size=35, color=colors, line=dict(width=1, color='black')),
        hoverinfo='text'
    ))
    fig.update_layout(geo=dict(showland=True, landcolor="rgb(200,230,201)", showcountries=True, countrycolor="rgb(100,100,100)", projection_type='natural earth'), margin={"r":0,"t":0,"l":0,"b":0}, height=1000)
    st.plotly_chart(fig, use_container_width=True)
