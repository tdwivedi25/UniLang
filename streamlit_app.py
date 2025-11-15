import streamlit as st
import plotly.graph_objects as go
import random

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- Initialize session state ----
if "page" not in st.session_state:
    st.session_state.page = "Unity Hub"
if "map_submissions" not in st.session_state:
    st.session_state.map_submissions = []

# ---- Sidebar Navigation ----
if st.sidebar.button("Unity Hub"):
    st.session_state.page = "Unity Hub"
if st.sidebar.button("Language Lab"):
    st.session_state.page = "Language Lab"
if st.sidebar.button("Top Voices"):
    st.session_state.page = "Top Voices"
if st.sidebar.button("World of Words"):
    st.session_state.page = "World of Words"

# ---- Local Images ----
home_header = "logo.png"
other_header = "header.jpg"

# ---- Sample Expressions Database ----
expressions = [
    {
        "input": "Break a leg",
        "translations": {
            "French": "Bonne chance",
            "German": "Viel Glück",
            "Spanish": "Buena suerte",
            "English": "Break a leg",
            "Japanese": "頑張って"
        },
        "type": "Idiom",
        "countries": ["United States","United Kingdom","Germany","France","Spain"]
    },
    {
        "input": "Why did the chicken cross the road?",
        "translations": {
            "French": "Pourquoi le poulet a traversé la route?",
            "German": "Warum ging das Huhn über die Straße?",
            "Spanish": "¿Por qué cruzó la gallina la carretera?",
            "English": "Why did the chicken cross the road?",
            "Japanese": "なぜ鶏は道路を渡ったのか？"
        },
        "type": "Joke",
        "countries": ["United States","Brazil","Japan","France","Germany"]
    },
    {
        "input": "Hit the sack",
        "translations": {
            "French": "Aller au lit",
            "German": "Ins Bett gehen",
            "Spanish": "Ir a la cama",
            "English": "Hit the sack",
            "Japanese": "寝る"
        },
        "type": "Idiom",
        "countries": ["United States","United Kingdom","France","Germany","Spain"]
    }
]

supported_languages = ["English", "French", "German", "Spanish", "Japanese"]

# ---- HELPER FUNCTIONS ----
def update_map(expression_entry):
    for country in expression_entry["countries"]:
        st.session_state.map_submissions.append((country, expression_entry["type"]))

def get_top_country():
    country_counts = {}
    for country, _ in st.session_state.map_submissions:
        country_counts[country] = country_counts.get(country, 0) + 1
    if not country_counts:
        return None, 0
    top_country = max(country_counts, key=country_counts.get)
    return top_country, country_counts[top_country]

# ---------------------- UNITY HUB ----------------------
if st.session_state.page == "Unity Hub":
    st.markdown(f"<div style='text-align:center; margin-bottom:30px;'><img src='{home_header}' style='width:300px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #1F77B4; font-size: 60px;'>Welcome to <b>Unilang</b>! 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF7F0E; font-size: 28px;'>Where languages and cultures unite!</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:20px; line-height:1.8; margin-bottom:20px;'>🚀 <b>Explore idioms and jokes from around the world</b><br>🗣️ <b>Learn how expressions are translated in different languages</b><br>🌟 <b>Discover the most popular phrases and share your favorites</b></div>", unsafe_allow_html=True)
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
    
    # Animated Emoji
    st.markdown("""
        <style>
        @keyframes bounce {0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);}}
        .bounce {display: inline-block; animation: bounce 1s infinite;}
        </style>
        <p style='text-align:center; font-size:40px;'><span class='bounce'>🌐✨🎉</span></p>
        """, unsafe_allow_html=True)

# ------------------- LANGUAGE LAB -------------------
elif st.session_state.page == "Language Lab":
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>", unsafe_allow_html=True)
    st.header("🔄 Language Lab")
    
    # Select Joke or Idiom
    expr_type = st.radio("Select Type:", ["Joke", "Idiom"], horizontal=True)
    
    user_input = st.text_area("Enter a joke or idiom (any language):", "")
    target_lang = st.selectbox("Select target language:", supported_languages)
    
    if st.button("Translate"):
        # Find matching expression
        expression_entry = None
        for expr in expressions:
            if expr["type"] == expr_type and expr["input"].lower() == user_input.lower():
                expression_entry = expr
                break
        # Fallback: random match if not exact
        if not expression_entry:
            matches = [e for e in expressions if e["type"] == expr_type]
            expression_entry = random.choice(matches)
        
        # Translation with fallback
        translation = expression_entry["translations"].get(target_lang)
        if not translation:
            translation = random.choice(list(expression_entry["translations"].values()))
        
        # Unity Meter
        resemblance = random.randint(50,100)
        
        # Display Results
        st.markdown(f"### Translation: {translation}")
        st.markdown(f"**Unity Meter:** {resemblance}% similarity")
        top3_countries = random.sample(expression_entry["countries"], min(3, len(expression_entry["countries"])))
        st.markdown(f"**Top 3 countries with similar expression:** {', '.join(top3_countries)}")
        
        # Update Map
        update_map(expression_entry)

# -------------------- TOP VOICES --------------------
elif st.session_state.page == "Top Voices":
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>", unsafe_allow_html=True)
    st.header("🏆 Leadership Dashboard")
    
    # Top Jokes/Idioms
    st.subheader("🌟 Top Expressions")
    expr_count = {}
    for country, t in st.session_state.map_submissions:
        for expr in expressions:
            if expr["type"] == t:
                expr_count[expr["input"]] = expr_count.get(expr["input"], 0) + 1
    sorted_expr = sorted(expr_count.items(), key=lambda x: x[1], reverse=True)
    for expr, count in sorted_expr[:5]:
        st.markdown(f"- {expr} ({count} submissions)")
    
    # Most Humorous Country
    st.subheader("🌍 Most Humorous Country")
    country_counts = {}
    for country, _ in st.session_state.map_submissions:
        country_counts[country] = country_counts.get(country,0)+1
    if country_counts:
        fig = go.Figure(go.Bar(
            x=list(country_counts.keys()),
            y=list(country_counts.values()),
            marker_color=[f"rgb({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)})" for _ in country_counts]
        ))
        fig.update_layout(title="Most Humorous Country (by submissions)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No submissions yet.")

# ----------------------- WORLD OF WORDS -------------------------
elif st.session_state.page == "World of Words":
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><img src='{other_header}' style='width:600px;'></div>", unsafe_allow_html=True)
    st.header("🗺️ World of Words")
    st.write("Filter and explore idioms & jokes across countries!")

    # Filters
    filter_col, legend_col = st.columns([2,1])
    with filter_col:
        filter_type = st.radio("Filter by Type", ["All", "Idiom", "Joke"], horizontal=True)
    with legend_col:
        st.markdown("<p style='margin:0;'><span style='color:blue;'>● Idiom</span> &nbsp;&nbsp;<span style='color:orange;'>● Joke</span></p>", unsafe_allow_html=True)
    
    # Filter data
    filtered_subs = [s for s in expressions if filter_type=="All" or s["type"]==filter_type]
    
    lats, lons, colors, texts = [], [], [], []
    country_coords = {"United States":[38,-97],"United Kingdom":[54,-2],"France":[46,2],"Germany":[51,10],"Spain":[40,-4],"Brazil":[-10,-55],"Japan":[36,138]}
    for sub in filtered_subs:
        for country in sub["countries"]:
            if country in country_coords:
                lat, lon = country_coords[country]
                lats.append(lat)
                lons.append(lon)
                colors.append("blue" if sub["type"]=="Idiom" else "orange")
                top3_bullets = "<br>   - " + "<br>   - ".join([f"{c}: {expr['translations'].get('English','')}" for c in sub["countries"] if c in country_coords])
                hover_text = f"<b>{sub['input']}</b><br>• Type: {sub['type']}<br>• Top 3 countries: {top3_bullets}"
                texts.append(hover_text)
    
    fig = go.Figure(go.Scattergeo(
        lon=lons, lat=lats, text=texts, mode='markers',
        marker=dict(size=35, color=colors, line=dict(width=1,color='black')),
        hoverinfo='text'
    ))
    fig.update_layout(geo=dict(showland=True, landcolor="rgb(200,230,201)", showcountries=True, countrycolor="rgb(100,100,100)", projection_type='natural earth'), margin={"r":0,"t":0,"l":0,"b":0}, height=1000)
    st.plotly_chart(fig, use_container_width=True)
