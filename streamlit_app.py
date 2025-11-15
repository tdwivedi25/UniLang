import streamlit as st
import plotly.graph_objects as go

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="wide")

# ---- Initialize session state for page navigation ----
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---- SIDEBAR BUTTONS ----
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Translation"):
    st.session_state.page = "Translation"
if st.sidebar.button("Leaderboard"):
    st.session_state.page = "Leaderboard"
if st.sidebar.button("Map"):
    st.session_state.page = "Map"

# ---- IMAGE RENDER FUNCTIONS ----
# Uses: logo.png
def show_logo():
    st.markdown(
        """
        <div style='display: flex; justify-content: center; margin-bottom: 20px;'>
            <img src='logo.png' style='width: 220px; border-radius: 20px;'>
        </div>
        """,
        unsafe_allow_html=True
    )

# Uses: header.jpg
def show_header():
    st.markdown(
        """
        <div style='display: flex; justify-content: center; margin-bottom: 20px;'>
            <img src='header.jpg' style='width: 450px; border-radius: 20px;'>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- HOME PAGE ----
if st.session_state.page == "Home":
    show_logo()   # ← uses logo.png
    st.header("🏠 Home")
    st.write(
        """
        Welcome to Unilang!  
        Explore idioms and jokes from around the world.  
        Use the sidebar to navigate between screens.
        """
    )

# ---- TRANSLATION PAGE ----
elif st.session_state.page == "Translation":
    show_header()  # ← uses header.jpg
    st.header("🔄 Translation")
    st.write("This page will let users input expressions and see translations (coming soon).")

# ---- LEADERBOARD PAGE ----
elif st.session_state.page == "Leaderboard":
    show_header()  # ← uses header.jpg
    st.header("🏆 Leaderboard")
    st.write("This page will display the most popular idioms and jokes (coming soon).")

# ---- MAP PAGE ----
elif st.session_state.page == "Map":
    show_header()  # ← uses header.jpg
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

    # --- Sample map data ---
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

    filtered_subs = [
        sub for sub in submissions
        if filter_type=="All" or sub["type"]==filter_type
    ]

    lats, lons, colors, texts = [], [], [], []

    for sub in filtered_subs:
        for country in sub["countries"]:
            if country in country_coords:
                lats.append(country_coords[country][0])
                lons.append(country_coords[country][1])
                colors.append("blue" if sub["type"]=="Idiom" else "orange")

                countries_of_origin = ", ".join(sub["countries"])
                top3_bullets = "<br>   - " + "<br>   - ".join([f"{c}: {expr}" for c, expr in sub["top3"]])

                hover_text = (
                    f"<b>{sub['input']}</b><br>"
                    f"• Country of origin: {countries_of_origin}<br>"
                    f"• Literal: {sub['literal']}<br>"
                    f"• Similar:{top3_bullets}"
                )
                texts.append(hover_text)

    fig = go.Figure(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=texts,
        mode='markers',
        marker=dict(size=35, color=colors, line=dict(width=1, color='black')),
        hoverinfo='text',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
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
