import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- SESSION STATE INIT ----
if "page" not in st.session_state:
    st.session_state.page = "Unity Hub"
if "top_expressions" not in st.session_state:
    st.session_state.top_expressions = []  # store dict: {"expression","type","country","count"}
if "humor_counts" not in st.session_state:
    st.session_state.humor_counts = {"USA":0,"France":0,"Germany":0,"Brazil":0,"Japan":0}

# ---- SIDEBAR NAVIGATION ----
if st.sidebar.button("Unity Hub"): st.session_state.page = "Unity Hub"
if st.sidebar.button("Language Lab"): st.session_state.page = "Language Lab"
if st.sidebar.button("Top Voices"): st.session_state.page = "Top Voices"
if st.sidebar.button("World of Words"): st.session_state.page = "World of Words"

# ---- LOCAL IMAGES ----
home_header = "logo.png"
other_header = "header.jpg"

# ---- HANDLE HTML BUTTON CLICK (Get Started) ----
query_params = st.query_params
if query_params.get("page") == ["LanguageLab"]:
    st.session_state.page = "Language Lab"
    st.experimental_set_query_params()  # clear query params

# ======================= UNITY HUB =======================
if st.session_state.page == "Unity Hub":
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:30px;'>
            <img src="{home_header}" style="width:300px;">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style='text-align: center; color: #1F77B4; font-size: 60px;'>Welcome to <b>Unilang</b>! 🌍</h1>
        <h3 style='text-align: center; color: #FF7F0E; font-size: 28px;'>Where languages and cultures unite!</h3>
        <div style='text-align:center; font-size:20px; line-height:1.8; margin-bottom:20px;'>
        🚀 <b>Explore idioms and jokes from around the world</b><br>
        🗣️ <b>Learn how expressions are translated in different languages</b><br>
        🌟 <b>Discover the most popular phrases and share your favorites</b>
        </div>
        <hr>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center; margin:30px 0;'>
            <form action="?page=LanguageLab">
                <input type="submit" value="🎯 Get Started!" 
                style="
                    background-color:#1F77B4; 
                    color:white; 
                    font-size:24px; 
                    padding:15px 40px; 
                    border:none; 
                    border-radius:12px; 
                    cursor:pointer;
                ">
            </form>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        @keyframes bounce {
            0%, 100% {transform: translateY(0);}
            50% {transform: translateY(-10px);}
        }
        .bounce { display: inline-block; animation: bounce 1s infinite; }
        </style>
        <p style='text-align:center; font-size:40px;'><span class='bounce'>🌐✨🎉</span></p>
        """, unsafe_allow_html=True)

# ==================== LANGUAGE LAB =====================
elif st.session_state.page == "Language Lab":
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:20px;'>
            <img src="{other_header}" style="width:600px;">
        </div>
        """, unsafe_allow_html=True)

    st.header("🔄 Language Lab")

    # --- SAMPLE DATA ---
    expressions = [
        {"text": "Break a leg", "type": "Idiom", "country": "USA", "translations": {"France":"Bonne chance","Germany":"Viel Glück","Spain":"Buena suerte","Japan":"頑張って"}},
        {"text": "Why did the chicken cross the road?", "type": "Joke", "country": "USA", "translations": {"France":"Pourquoi le poulet a traversé la route?","Germany":"Warum ging das Huhn über die Straße?","Brazil":"Por que a galinha atravessou a estrada?","Japan":"なぜ鶏は道を渡ったのか？"}},
        {"text": "Hit the sack", "type": "Idiom", "country": "USA", "translations": {"France":"Aller au lit","Germany":"Ins Bett gehen","Spain":"Ir a la cama","Japan":"寝る"}},
    ]
    target_languages = ["English","French","German","Spanish","Japanese","Brazilian Portuguese"]

    # --- USER INPUT ---
    expr_type = st.selectbox("Select type:", ["Idiom","Joke"])
    user_input = st.text_input(f"Enter your {expr_type.lower()}:")
    target_lang = st.selectbox("Select target language:", target_languages)

    if st.button("Translate"):
        if user_input.strip() == "":
            st.warning("Please enter a phrase to translate!")
        else:
            # Pick a random sample for similarity
            translation_entry = random.choice([e for e in expressions if e["type"]==expr_type])
            translation = translation_entry["translations"].get(target_lang,"(Translation not available)")
            unity_pct = random.randint(50,95)
            top3 = random.sample(list(translation_entry["translations"].items()), k=3)

            # Display results
            st.subheader("Translation:")
            st.success(f"{translation}")
            st.subheader("Unity Meter:")
            st.progress(unity_pct)
            st.subheader("Top 3 countries with similar expression:")
            for c, t in top3:
                st.write(f"🌍 {c}: {t}")

            # --- UPDATE TOP EXPRESSIONS ---
            found = False
            for e in st.session_state.top_expressions:
                if e["expression"]==user_input and e["type"]==expr_type:
                    e["count"] += 1
                    found = True
                    break
            if not found:
                st.session_state.top_expressions.append({
                    "expression": user_input,
                    "type": expr_type,
                    "country": translation_entry["country"],
                    "count": 1
                })
            
            # --- UPDATE HUMOR COUNTS ---
            country = translation_entry["country"]
            st.session_state.humor_counts[country] += 1

# ==================== TOP VOICES / LEADERSHIP DASHBOARD =====================
elif st.session_state.page == "Top Voices":
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:20px;'>
            <img src="{other_header}" style="width:600px;">
        </div>
        """, unsafe_allow_html=True)

    st.header("🏆 Leadership Dashboard")

    # --- Display Top Expressions ---
    if st.session_state.top_expressions:
        top_df = pd.DataFrame(st.session_state.top_expressions)
        top_df = top_df.sort_values("count", ascending=False)
        st.subheader("Top Jokes & Idioms Worldwide")
        st.dataframe(top_df[["expression","type","country","count"]])
    else:
        st.info("No submissions yet. Go to Language Lab and submit a joke or idiom!")

    # --- Humor Country Bar Chart ---
    humor_counts = pd.DataFrame([
        {"country":c,"jokes":cnt} for c,cnt in st.session_state.humor_counts.items()
    ])
    st.subheader("Most Humorous Countries")
    fig = go.Figure([go.Bar(x=humor_counts['country'], y=humor_counts['jokes'],
                            marker_color=['#1F77B4','#FF7F0E','#2CA02C','#D62728','#9467BD'])])
    fig.update_layout(yaxis_title="Number of Funny Expressions", xaxis_title="Country")
    st.plotly_chart(fig, use_container_width=True)

# ==================== WORLD OF WORDS =====================
elif st.session_state.page == "World of Words":
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:20px;'>
            <img src="{other_header}" style="width:600px;">
        </div>
        """, unsafe_allow_html=True)
    
    st.header("🗺️ World of Words")
    st.write("Filter and explore idioms & jokes across countries!")

    filter_col, legend_col = st.columns([2,1])
    with filter_col:
        filter_type = st.radio("Filter by Type", ["All", "Idiom", "Joke"], horizontal=True)
    with legend_col:
        st.markdown("<p style='margin:0;'><span style='color:blue;'>● Idiom</span> &nbsp;&nbsp; <span style='color:orange;'>● Joke</span></p>", unsafe_allow_html=True)

    # --- Sample submissions from top expressions ---
    submissions = st.session_state.top_expressions
    country_coords = {
        "USA":[38,-97],"France":[46,2],"Germany":[51,10],"Brazil":[-10,-55],"Japan":[36,138]
    }

    filtered_subs = [sub for sub in submissions if filter_type=="All" or sub["type"]==filter_type]
    lats, lons, colors, texts = [], [], [], []
    for sub in filtered_subs:
        country = sub["country"]
        if country in country_coords:
            lat, lon = country_coords[country]
            lats.append(lat)
            lons.append(lon)
            colors.append("blue" if sub["type"]=="Idiom" else "orange")
            texts.append(f"<b>{sub['expression']}</b><br>Type: {sub['type']}<br>Count: {sub['count']}")

    fig = go.Figure(go.Scattergeo(lon=lons, lat=lats, text=texts, mode='markers',
                                  marker=dict(size=35, color=colors, line=dict(width=1, color='black')),
                                  hoverinfo='text'))
    fig.update_layout(
        geo=dict(showland=True, landcolor="rgb(200,230,201)", showcountries=True, countrycolor="rgb(100,100,100)", projection_type='natural earth'),
        margin={"r":0,"t":0,"l":0,"b":0}, height=1000
    )
    st.plotly_chart(fig, use_container_width=True)
