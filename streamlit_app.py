import streamlit as st
import plotly.graph_objects as go

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- Initialize session state for page navigation ----
if "page" not in st.session_state:
    st.session_state.page = "Unity Hub"

# ---- SIDEBAR BUTTON NAVIGATION ----
if st.sidebar.button("Unity Hub"):
    st.session_state.page = "Unity Hub"
if st.sidebar.button("Language Lab"):
    st.session_state.page = "Language Lab"
if st.sidebar.button("Top Voices"):
    st.session_state.page = "Top Voices"
if st.sidebar.button("World of Words"):
    st.session_state.page = "World of Words"

# ---- LOCAL IMAGES ----
home_header = "logo.png"       # 🟦 Unity Hub
other_header = "header.jpg"    # 🟩 All other pages

# ---------------------- UNITY HUB ----------------------
if st.session_state.page == "Unity Hub":
    # Display logo
    st.image(home_header, width=180)

    st.markdown(
        """
        <h1 style='text-align: center; color: #1F77B4;'>Welcome to <b>Unilang</b>! 🌍</h1>
        <h3 style='text-align: center; color: #FF7F0E;'>Where languages and cultures unite!</h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='text-align:center; font-size:18px; line-height:1.8;'>
        🚀 <b>Explore idioms and jokes from around the world</b><br>
        🗣️ <b>Learn how expressions are translated in different languages</b><br>
        🌟 <b>Discover the most popular phrases and share your favorites</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Centered Get Started Button using Streamlit
    if st.button("🎯 Get Started!"):
        st.session_state.page = "Language Lab"

    # Animated Emoji Effect (CSS)
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
        <p style='text-align:center; font-size:30px;'><span class='bounce'>🌐✨🎉</span></p>
        """,
        unsafe_allow_html=True
    )

# ------------------- LANGUAGE LAB -------------------
elif st.session_state.page == "Language Lab":
    st.image(other_header, width=450)
    st.header("🔄 Language Lab")
    st.write("This page will let users input expressions and see translations (coming soon).")

# -------------------- TOP VOICES --------------------
elif st.session_state.page == "Top Voices":
    st.image(other_header, width=450)
    st.header("🏆 Top Voices")
    st.write("This page will display the most popular idioms and jokes (coming soon).")

# ----------------------- WORLD OF WORDS -------------------------
elif st.session_state.page == "World of Words":
    st.image(other_header, width=450)
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

    country_coords = {
        "United States":[38,-97],
        "United Kingdom":[54,-2],
        "France":[46,2],
        "Germany":[51,10],
        "Spain":[40,-4],
        "Brazil":[-10,-55],
        "Japan":[36,138]
    }

    # --- Filter logic ---
    filtered_subs = [
        sub for sub in submissions
        if filter_type=="All" or sub["type"]==filter_type
    ]

    lats, lons, colors, texts = [], [], [], []

    for sub in filtered_subs:
        for country in sub["countries"]:
            if country in country_coords:
                lat, lon = country_coords[country]
                lats.append(lat)
                lons.append(lon)
                colors.append("blue" if sub["type"]=="Idiom" else "orange")

                top3_bullets = "<br>   - " + "<br>   - ".join([f"{c}: {expr}" for c, expr in sub["top3"]])

                hover_text = (
                    f"<b>{sub['input']}</b><br>"
                    f"• Literal: {sub['literal']}<br>"
                    f"• Similar: {top3_bullets}"
                )
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
