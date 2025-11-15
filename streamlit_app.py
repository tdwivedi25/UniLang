import streamlit as st
import plotly.graph_objects as go

# ---- APP CONFIG ----
st.set_page_config(page_title="Unilang", page_icon="🌍", layout="centered")

# ---- HEADER ----
st.image(
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfd5j0K8WAz8so_1o2VVLWW8uZ77kwzr_8kg&s",
    use_column_width=True,
)
st.title("🌍 Unilang")
st.subheader("Unity through language — explore idioms and jokes across the world!")
st.write("Welcome! Select what you want to do below.")

# ---- SIDEBAR ----
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Translation", "Leaderboard", "Map"])

# ---- HOME PAGE ----
if page == "Home":
    st.header("🏠 Home")
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfd5j0K8WAz8so_1o2VVLWW8uZ77kwzr_8kg&s",
        use_column_width=True,
    )
    st.write(
        """
        Unilang is a platform for:
        - Exploring idioms and jokes across the world  
        - Learning how expressions vary by culture  
        - Seeing translations and humorous equivalents  
        """
    )

# ---- TRANSLATION PAGE ----
elif page == "Translation":
    st.header("🔄 Translation")
    st.write("Translation page coming soon! Users will input expressions and see translations here.")

# ---- LEADERBOARD PAGE ----
elif page == "Leaderboard":
    st.header("🏆 Leaderboard")
    st.write("Leaderboard page coming soon! Popular idioms and jokes will appear here.")

# ---- MAP PAGE ----
elif page == "Map":
    st.header("🗺️ World Map of Idioms & Jokes")

    # --- Filters and legend ---
    filter_col, legend_col = st.columns([2,1])
    with filter_col:
        filter_type = st.radio("Filter by Type", ["All", "Idiom", "Joke"], horizontal=True)
    with legend_col:
        st.markdown("<p style='margin:0;'><span style='color:blue;'>● Idiom</span> &nbsp;&nbsp; <span style='color:orange;'>● Joke</span></p>", unsafe_allow_html=True)

    # --- Sample data ---
    submissions = [
        {"input": "Break a leg", "literal": "Wish you luck", "type": "Idiom",
         "countries": ["United States","United Kingdom","Germany","France"],
         "top3": [("France","Bonne chance"),("Germany","Viel Glück"),("Spain","Buena suerte")]},
        {"input": "Why did the chicken cross the road?", "literal": "A classic joke", "type": "Joke",
         "countries": ["United States","Brazil","Japan"],
         "top3": [("France","Pourquoi le poulet a traversé la route?"),("Germany","Warum ging das Huhn über die Straße?"),("Brazil","Por que a galinha atravessou a estrada?")]},
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

    filtered_subs = [sub for sub in submissions if filter_type=="All" or sub["type"]==filter_type]

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
