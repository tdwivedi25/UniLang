import streamlit as st
import plotly.graph_objects as go

# --- Remove default Streamlit padding/margins ---
st.markdown("""
    <style>
        .css-18e3th9 {padding-top: 0rem;}
        .css-1d391kg {padding-top: 0rem;}
        .css-1v3fvcr {padding-bottom: 0rem;}
        .block-container {padding-top:0rem; padding-bottom:0rem;}
    </style>
""", unsafe_allow_html=True)

# --- Header image ---
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfd5j0K8WAz8so_1o2VVLWW8uZ77kwzr_8kg&s"
st.image(image_url, use_column_width=True)

# --- Title / subtitle ---
st.markdown("<h1 style='text-align:center; margin-bottom:0;'>🌍 Unilang - World Map</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; margin-top:0; margin-bottom:10px;'>Unity through language — see how expressions connect globally!</p>", unsafe_allow_html=True)

# --- Filters and legend on main screen ---
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
    {"input": "Piece of cake", "literal": "Something very easy", "type": "Idiom",
     "countries": ["United States","United Kingdom","Spain","France","Germany"],
     "top3": [("France","C'est du gâteau"),("Germany","Kinderspiel"),("Spain","Pan comido")]},
    {"input": "When pigs fly", "literal": "Something impossible", "type": "Idiom",
     "countries": ["United States","United Kingdom","Spain"],
     "top3": [("France","Quand les poules auront des dents"),("Germany","Wenn Schweine fliegen"),("Spain","Cuando las ranas críen pelo")]},
    {"input": "Knock knock. Who’s there?", "literal": "Classic joke setup", "type": "Joke",
     "countries": ["United Kingdom","United States","Japan"],
     "top3": [("France","Toc, toc, qui est là?"),("Germany","Klopf, klopf, wer ist da?"),("Japan","誰かいる？")]}
]

# --- Map coordinates for full country names ---
country_coords = {
    "United States":[38,-97],
    "United Kingdom":[54,-2],
    "France":[46,2],
    "Germany":[51,10],
    "Spain":[40,-4],
    "Brazil":[-10,-55],
    "Japan":[36,138]
}

# --- Filter submissions ---
filtered_subs = [sub for sub in submissions if filter_type=="All" or sub["type"]==filter_type]

# --- Map data ---
lats, lons, colors, texts = [], [], [], []

for sub in filtered_subs:
    for country in sub["countries"]:
        if country in country_coords:
            lats.append(country_coords[country][0])
            lons.append(country_coords[country][1])
            colors.append("blue" if sub["type"]=="Idiom" else "orange")
            # Hover text with country of origin + literal + top 3 expressions (country + expression)
            countries_of_origin = ", ".join(sub["countries"])
            top3_bullets = "<br>   - " + "<br>   - ".join([f"{c}: {expr}" for c, expr in sub["top3"]])
            hover_text = (
                f"<b>{sub['input']}</b><br>"
                f"• Country of origin: {countries_of_origin}<br>"
                f"• Literal: {sub['literal']}<br>"
                f"• Similar:{top3_bullets}"
            )
            texts.append(hover_text)

# --- Create map ---
fig = go.Figure(go.Scattergeo(
    lon=lons,
    lat=lats,
    text=texts,
    mode='markers',
    marker=dict(size=35, color=colors, line=dict(width=1, color='black')),
    hoverinfo='text',
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial"
    )
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

# --- Display map ---
st.plotly_chart(fig, use_container_width=True)
