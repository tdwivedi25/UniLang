import streamlit as st
import plotly.graph_objects as go

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- Initialize session state for page navigation ----
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---- SIDEBAR BUTTON NAVIGATION ----
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Translation"):
    st.session_state.page = "Translation"
if st.sidebar.button("Leaderboard"):
    st.session_state.page = "Leaderboard"
if st.sidebar.button("Map"):
    st.session_state.page = "Map"

# ---- LOCAL IMAGES ----
home_header = "logo.png"       # 🟦 Home
other_header = "header.jpg"    # 🟩 All other pages

# ---------------------- HOME PAGE ----------------------
if st.session_state.page == "Home":
    st.image(home_header, use_column_width=True)
    st.header("🏠 Home")
    st.write(
        """
        Welcome to Unilang!  
        Explore idioms and jokes from around the world.  
        Use the sidebar to navigate between screens.
        """
    )

# ------------------- TRANSLATION PAGE -------------------
elif st.session_state.page == "Translation":
    st.image(other_header, use_column_width=True)
    st.header("🔄 Translation")
    st.write("This page will let users input expressions and see translations (coming soon).")

# -------------------- LEADERBOARD PAGE --------------------
elif st.session_state.page == "Leaderboard":
    st.image(other_header, use_column_width=True)
    st.header("🏆 Leaderboard")
    st.write("This page will display the most popular idioms and jokes (coming soon).")

# ----------------------- MAP PAGE -------------------------
elif st.session_state.page == "Map":
    st.image(other_header, use_column_width=True)
    st.header("🗺️ World Map of Idioms & Jokes")
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
