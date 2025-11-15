import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- SESSION STATE ----
if "page" not in st.session_state:
    st.session_state.page = "Unity Hub"

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

# ---- HANDLE HTML BUTTON CLICK ----
query_params = st.experimental_get_query_params()
if query_params.get("page") == ["LanguageLab"]:
    st.session_state.page = "Language Lab"
    st.experimental_set_query_params()  # clear query params

# ---------------------- UNITY HUB ----------------------
if st.session_state.page == "Unity Hub":
    # Centered Logo
    st.markdown(
        f"""
        <div style='text-align:center; margin-bottom:30px;'>
            <img src="{home_header}" style="width:300px;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Welcome Text
    st.markdown(
        """
        <h1 style='text-align: center; color: #1F77B4; font-size: 60px;'>Welcome to <b>Unilang</b>! 🌍</h1>
        <h3 style='text-align: center; color: #FF7F0E; font-size: 28px;'>Where languages and cultures unite!</h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='text-align:center; font-size:20px; line-height:1.8; margin-bottom:20px;'>
        🚀 <b>Explore idioms and jokes from around the world</b><br>
        🗣️ <b>Learn how expressions are translated in different languages</b><br>
        🌟 <b>Discover the most popular phrases and share your favorites</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ---- Fully Centered HTML Get Started Button ----
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )

    # Animated Emoji
    st.markdown(
        """
        <style>
        @keyframes bounce {
            0%, 100% {transform: translateY(0);}
            50% {transform: translateY(-10px);}
        }
        .bounce {
            display: inline-block;
            animation: bounce 1s infinite;
        }
        </style>
        <p style='text-align:center; font-size:40px;'><span class='bounce'>🌐✨🎉</span></p>
        """,
        unsafe_allow_html=True
    )

# ------------------- LANGUAGE LAB -------------------
elif st.session_state.page == "Language Lab":
    st.markdown(
        f"""
        <div style='text-align:center; margin-bottom:20px;'>
            <img src="{other_header}" style="width:600px;">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.header("🔄 Language Lab")
    st.write("This page will let users input expressions and see translations (coming soon).")

# -------------------- TOP VOICES / LEADERSHIP DASHBOARD --------------------
elif st.session_state.page == "Top Voices":
    st.markdown(
        f"""
        <div style='text-align:center; margin-bottom:20px;'>
            <img src="{other_header}" style="width:600px;">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.header("🏆 Leadership Dashboard")

    # ----- Sample Data -----
    users = pd.DataFrame([
        {"user": "Alice", "country": "USA", "points": 120},
        {"user": "Bob", "country": "Germany", "points": 150},
        {"user": "Chloe", "country": "France", "points": 130},
        {"user": "Diego", "country": "Brazil", "points": 170},
        {"user": "Eiko", "country": "Japan", "points": 140}
    ])

    jokes_idioms = pd.DataFrame([
        {"text": "Break a leg", "type": "Idiom", "country": "USA"},
        {"text": "Pourquoi le poulet a traversé la route?", "type": "Joke", "country": "France"},
        {"text": "Viel Glück", "type": "Idiom", "country": "Germany"},
        {"text": "Por que a galinha atravessou a estrada?", "type": "Joke", "country": "Brazil"},
        {"text": "頑張ってね", "type": "Idiom", "country": "Japan"}
    ])

    # ----- User Leaderboard -----
    st.subheader("🌍 Top Users by Country")
    top_users = users.sort_values("points", ascending=False)
    st.table(top_users)

    # ----- Top Jokes / Idioms -----
    st.subheader("😂 Top Jokes & Idioms (Global)")
    st.table(jokes_idioms)

    # ----- Most Humorous Country Bar Chart -----
    st.subheader("📊 Most Humorous Country")
    country_counts = jokes_idioms["country"].value_counts()
    fig = go.Figure(go.Bar(
        x=country_counts.index,
        y=country_counts.values,
        marker_color='orange'
    ))
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Number of Jokes / Idioms",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------- WORLD OF WORDS -------------------------
elif st.session_state.page == "World of Words":
    st.markdown(
        f"""
        <div style='text-align:center; margin-bottom:20px;'>
            <img src="{other_header}" style="width:600px;">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.header("🗺️ World of Words")
    st.write("Filter and explore idioms & jokes across countries!")

    # --- Filters ---
    filter_col, legend_col = st.columns([2,1])
    with filter_col:
        filter_type = st.radio("Filter by Type", ["All", "Idiom", "Joke"], horizontal=True)
    with legend_col:
        st.markdown(
            "<p style='margin:0;'><span style='color:blue;'>● Idiom</span> &nbsp;&nbsp; "
            "<span style='color:orange;'>● Joke</span></p>",
            unsafe_allow_html=True
        )

    # --- Sample Data ---
    submissions = [
        {"input": "Break a leg", "literal": "Wish you luck", "type": "Idiom", "countries": ["USA","UK","Germany","France"], "top3": [("France","Bonne chance"),("Germany","Viel Glück"),("Spain","Buena suerte")]},
        {"input": "Why did the chicken cross the road?", "literal": "A classic joke", "type": "Joke", "countries": ["USA","Brazil","Japan"], "top3": [("France","Pourquoi le poulet a traversé la route?"),("Germany","Warum ging das Huhn über die Straße?"),("Brazil","Por que a galinha atravessou a estrada?")]}
    ]

    country_coords = {"USA":[38,-97],"UK":[54,-2],"France":[46,2],"Germany":[51,10],"Spain":[40,-4],"Brazil":[-10,-55],"Japan":[36,138]}

    filtered_subs = [sub for sub in submissions if filter_type=="All" or sub["type"]==filter_type]

    lats, lons, colors, texts = [], [], [], []
    for sub in filtered_subs:
        for country in sub["countries"]:
            if country in country_coords:
                lat, lon = country_coords[country]
                lats.append(lat)
                lons.append(lon)
                colors.append("blue" if sub["type"]=="Idiom" else "orange")
                top3_bullets = "<br>   - " + "<br>   - ".join([f"{c}: {expr}" for c, expr in sub["top3"]])
                hover_text = f"<b>{sub['input']}</b><br>• Literal: {sub['literal']}<br>• Similar: {top3_bullets}"
                texts.append(hover_text)

    fig = go.Figure(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=texts,
        mode='markers',
        marker=dict(size=35, color=colors, line=dict(width=1, color='black')),
        hoverinfo='text'
    ))

    fig.update_layout(
        geo=dict(showland=True, landcolor="rgb(200,230,201)", showcountries=True, countrycolor="rgb(100,100,100)", projection_type='natural earth'),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=1000
    )

    st.plotly_chart(fig, use_container_width=True)
