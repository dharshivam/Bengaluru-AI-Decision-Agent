import streamlit as st
import requests

from datetime import datetime, time, timedelta

from ml.predict import predict_travel_time

from agents.decision_agent import (
    make_journey_decision
)

from agents.weather_agent import (
    get_weather
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bengaluru AI Urban Decision Agent",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SAFE HTML RENDERER
# =========================================================

def render_html(html_str):

    lines = [
        line.strip()
        for line in html_str.strip("\n").split("\n")
        if line.strip() != ""
    ]

    st.markdown(
        "\n".join(lines),
        unsafe_allow_html=True
    )


# =========================================================
# PROFESSIONAL UI STYLING
# =========================================================

render_html("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Manrope:wght@600;700;800&display=swap'
);

html,
body,
[class*="css"] {
    font-family:
        'Inter',
        -apple-system,
        BlinkMacSystemFont,
        sans-serif;
}

* {
    scrollbar-width: thin;
    scrollbar-color: #2b3c56 #0a1220;
}

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #0a1220;
}

::-webkit-scrollbar-thumb {
    background:
        linear-gradient(
            180deg,
            #3b82f6,
            #2563eb
        );
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #60a5fa;
}


/* =====================================================
   ANIMATIONS
   ===================================================== */

@keyframes fadeInUp {

    from {
        opacity: 0;
        transform: translateY(14px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}

@keyframes softPulse {

    0%, 100% {
        box-shadow:
            0 0 0 0
            rgba(34, 197, 94, 0.35);
    }

    50% {
        box-shadow:
            0 0 0 6px
            rgba(34, 197, 94, 0);
    }

}


/* =====================================================
   GLOBAL
   ===================================================== */

html,
body {
    background-color: #070f1c !important;
}

.stApp {

    background:

        radial-gradient(
            circle at 0% 0%,
            rgba(59, 130, 246, 0.12),
            transparent 32%
        ),

        radial-gradient(
            circle at 100% 0%,
            rgba(45, 212, 191, 0.10),
            transparent 30%
        ),

        radial-gradient(
            circle at 50% 100%,
            rgba(139, 92, 246, 0.06),
            transparent 40%
        ),

        linear-gradient(
            180deg,
            #070f1c 0%,
            #0a1220 50%,
            #070e1a 100%
        );

    color: #e5e7eb;
}

header[data-testid="stHeader"] {

    background:
        #070f1c !important;

    border-bottom:
        1px solid #1e293b;
}

div[data-testid="stAppViewContainer"] {
    background:
        transparent !important;
}

div[data-testid="stMainBlockContainer"],
div[data-testid="stMain"] {
    background:
        transparent !important;
}

header[data-testid="stHeader"] * {
    color: #e5e7eb !important;
}

.block-container {

    max-width: 1450px;

    padding-top: 2rem;

    padding-bottom: 3rem;

    animation:
        fadeInUp 0.5s ease both;
}

h1,
h2,
h3,
h4 {

    font-family:
        'Manrope',
        'Inter',
        sans-serif;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {

    background:

        linear-gradient(
            180deg,
            #0c1729 0%,
            #081220 100%
        );

    border-right:
        1px solid #1e293b;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color: #f8fafc;

    font-weight: 800;

    font-family:
        'Manrope',
        sans-serif;
}

section[data-testid="stSidebar"] label {

    color: #cbd5e1 !important;

    font-weight: 600;
}

section[data-testid="stSidebar"] .stCaption {
    color: #64748b;
}

section[data-testid="stSidebar"] hr {

    margin: 18px 0;

    opacity: 0.5;
}


/* =====================================================
   HERO
   ===================================================== */

.hero {

    position: relative;

    overflow: hidden;

    padding: 42px 46px;

    border-radius: 28px;

    background:

        linear-gradient(
            135deg,
            rgba(15, 28, 50, 0.98),
            rgba(20, 38, 67, 0.96)
        );

    border:
        1px solid
        rgba(71, 85, 105, 0.60);

    box-shadow:

        0 30px 80px
        rgba(0, 0, 0, 0.32),

        inset 0 1px 0
        rgba(255, 255, 255, 0.04);

    margin-bottom: 32px;

    animation:
        fadeInUp 0.6s ease both;
}

.hero::before {

    content: "";

    position: absolute;

    width: 380px;

    height: 380px;

    right: -160px;

    top: -180px;

    border-radius: 50%;

    background:

        radial-gradient(
            circle,
            rgba(56, 189, 248, 0.20),
            transparent 70%
        );
}

.hero::after {

    content: "";

    position: absolute;

    width: 260px;

    height: 260px;

    left: -140px;

    bottom: -160px;

    border-radius: 50%;

    background:

        radial-gradient(
            circle,
            rgba(99, 102, 241, 0.17),
            transparent 70%
        );
}

.hero-small {

    position: relative;

    z-index: 2;

    color: #38bdf8;

    font-size: 12px;

    font-weight: 850;

    letter-spacing: 2px;

    text-transform: uppercase;

    margin-bottom: 12px;
}

.hero-title {

    position: relative;

    z-index: 2;

    color: #f8fafc;

    font-family:
        'Manrope',
        sans-serif;

    font-size: 44px;

    font-weight: 900;

    letter-spacing: -1.8px;

    line-height: 1.12;

    margin-bottom: 14px;

    background:

        linear-gradient(
            90deg,
            #f8fafc 60%,
            #93c5fd 100%
        );

    -webkit-background-clip: text;

    background-clip: text;
}

.hero-description {

    position: relative;

    z-index: 2;

    color: #94a3b8;

    font-size: 15px;

    line-height: 1.75;

    max-width: 900px;
}

.online-pill {

    position: relative;

    z-index: 2;

    display: inline-block;

    margin-top: 20px;

    padding: 8px 16px;

    border-radius: 50px;

    background:
        rgba(34, 197, 94, 0.10);

    border:
        1px solid
        rgba(34, 197, 94, 0.30);

    color: #86efac;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 0.5px;

    animation:
        softPulse 2.6s ease-in-out infinite;
}


/* =====================================================
   SECTION TITLES
   ===================================================== */

.section-title {

    position: relative;

    color: #f8fafc;

    font-family:
        'Manrope',
        sans-serif;

    font-size: 24px;

    font-weight: 850;

    letter-spacing: -0.4px;

    margin-top: 30px;

    margin-bottom: 8px;

    padding-left: 14px;
}

.section-title::before {

    content: "";

    position: absolute;

    left: 0;

    top: 4px;

    bottom: 4px;

    width: 4px;

    border-radius: 4px;

    background:

        linear-gradient(
            180deg,
            #38bdf8,
            #6366f1
        );
}

.section-subtitle {

    color: #64748b;

    font-size: 13px;

    line-height: 1.6;

    margin-bottom: 20px;

    padding-left: 14px;
}


/* =====================================================
   INPUTS
   ===================================================== */

div[data-baseweb="select"] > div {

    background:
        #111c30 !important;

    border:
        1px solid #2b3c56 !important;

    border-radius:
        13px !important;

    min-height: 48px;

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

div[data-baseweb="select"] > div:hover {

    border-color:
        #3b82f6 !important;

    box-shadow:
        0 0 0 3px
        rgba(59, 130, 246, 0.12);
}

input {

    background:
        #111c30 !important;

    color:
        #f8fafc !important;

    border-radius:
        12px !important;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stTimeInput"] input {

    border:
        1px solid #2b3c56 !important;

    transition:
        border-color 0.2s ease;
}

div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTimeInput"] input:focus {

    border-color:
        #3b82f6 !important;
}


/* =====================================================
   BUTTON
   ===================================================== */

div.stButton > button {

    height: 58px;

    border-radius: 15px;

    border:
        1px solid
        rgba(96, 165, 250, 0.30);

    background:

        linear-gradient(
            135deg,
            #2563eb,
            #4f46e5
        );

    color: white;

    font-size: 16px;

    font-weight: 850;

    letter-spacing: 0.3px;

    box-shadow:
        0 14px 32px
        rgba(37, 99, 235, 0.28);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        filter 0.2s ease;
}

div.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 20px 44px
        rgba(37, 99, 235, 0.38);

    border-color:
        rgba(147, 197, 253, 0.55);

    filter:
        brightness(1.06);
}

div.stButton > button:active {

    transform:
        translateY(0px)
        scale(0.99);
}


/* =====================================================
   AI CARD
   ===================================================== */

.ai-card {

    position: relative;

    overflow: hidden;

    margin-top: 28px;

    padding: 32px;

    border-radius: 24px;

    background:

        linear-gradient(
            135deg,
            rgba(6, 78, 59, 0.55),
            rgba(15, 23, 42, 0.96)
        );

    border:
        1px solid
        rgba(52, 211, 153, 0.32);

    box-shadow:
        0 24px 60px
        rgba(0, 0, 0, 0.26);

    animation:
        fadeInUp 0.5s ease both;
}

.ai-card::after {

    content: "";

    position: absolute;

    width: 240px;

    height: 240px;

    right: -95px;

    top: -105px;

    border-radius: 50%;

    background:

        radial-gradient(
            circle,
            rgba(52, 211, 153, 0.20),
            transparent 70%
        );
}

.ai-label {

    position: relative;

    z-index: 2;

    color: #6ee7b7;

    font-size: 12px;

    font-weight: 850;

    letter-spacing: 1.6px;

    text-transform: uppercase;
}

.ai-time {

    position: relative;

    z-index: 2;

    color: #ffffff;

    font-family:
        'Manrope',
        sans-serif;

    font-size: 46px;

    font-weight: 900;

    line-height: 1.15;

    margin-top: 8px;
}

.ai-text {

    position: relative;

    z-index: 2;

    color: #94a3b8;

    font-size: 14px;

    line-height: 1.75;

    margin-top: 10px;
}


/* =====================================================
   METRICS
   ===================================================== */

div[data-testid="stMetric"] {

    background:

        linear-gradient(
            145deg,
            #111c31,
            #0e1728
        );

    border:
        1px solid #26364e;

    border-radius: 19px;

    padding: 22px;

    min-height: 125px;

    box-shadow:
        0 12px 32px
        rgba(0, 0, 0, 0.16);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {

    transform:
        translateY(-4px);

    border-color:
        #3b82f6;

    box-shadow:
        0 20px 40px
        rgba(37, 99, 235, 0.18);
}

div[data-testid="stMetricLabel"] {

    color:
        #94a3b8 !important;

    font-size:
        12px !important;

    font-weight:
        700 !important;
}

div[data-testid="stMetricValue"] {

    color:
        #f8fafc !important;

    font-family:
        'Manrope',
        sans-serif;

    font-size:
        30px !important;

    font-weight:
        850 !important;
}


/* =====================================================
   WEATHER CARD
   ===================================================== */

.weather-card {

    background:

        linear-gradient(
            145deg,
            rgba(14, 116, 144, 0.20),
            rgba(15, 23, 42, 0.96)
        );

    border:
        1px solid
        rgba(56, 189, 248, 0.28);

    border-radius:
        20px;

    padding:
        24px;

    min-height:
        145px;

    box-shadow:
        0 15px 35px
        rgba(0, 0, 0, 0.18);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}

.weather-card:hover {

    transform:
        translateY(-3px);

    border-color:
        rgba(56, 189, 248, 0.55);
}

.weather-label {

    color:
        #67e8f9;

    font-size:
        11px;

    font-weight:
        850;

    letter-spacing:
        1.2px;

    text-transform:
        uppercase;
}

.weather-value {

    color:
        #f8fafc;

    font-family:
        'Manrope',
        sans-serif;

    font-size:
        27px;

    font-weight:
        900;

    margin-top:
        7px;
}

.weather-description {

    color:
        #94a3b8;

    font-size:
        12px;

    line-height:
        1.6;

    margin-top:
        5px;
}


/* =====================================================
   LOCATION CARDS
   ===================================================== */

.location-card {

    background:

        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.94),
            rgba(10, 18, 31, 0.94)
        );

    border:
        1px solid #26364e;

    border-radius:
        19px;

    padding:
        22px;

    min-height:
        120px;

    box-shadow:
        0 10px 28px
        rgba(0, 0, 0, 0.14);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}

.location-card:hover {

    transform:
        translateY(-3px);

    border-color:
        #3b506d;
}

.location-label {

    color:
        #64748b;

    font-size:
        11px;

    font-weight:
        800;

    letter-spacing:
        1px;

    margin-bottom:
        8px;
}

.location-name {

    color:
        #f8fafc;

    font-size:
        18px;

    font-weight:
        800;
}

.location-description {

    color:
        #64748b;

    font-size:
        11px;

    line-height:
        1.5;

    margin-top:
        6px;
}


/* =====================================================
   AGENT CARDS
   ===================================================== */

.agent-card {

    background:

        linear-gradient(
            145deg,
            #101b2d,
            #0d1727
        );

    border:
        1px solid #26364e;

    border-radius:
        18px;

    padding:
        21px;

    min-height:
        160px;

    box-shadow:
        0 10px 28px
        rgba(0, 0, 0, 0.14);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.agent-card:hover {

    transform:
        translateY(-4px);

    border-color:
        #3b82f6;

    box-shadow:
        0 18px 36px
        rgba(37, 99, 235, 0.16);
}

.agent-title {

    color:
        #f8fafc;

    font-size:
        15px;

    font-weight:
        800;

    margin-bottom:
        10px;
}

.agent-online {

    color:
        #4ade80;

    font-size:
        11px;

    font-weight:
        850;

    letter-spacing:
        0.8px;
}

.agent-next {

    color:
        #fbbf24;

    font-size:
        11px;

    font-weight:
        850;

    letter-spacing:
        0.8px;
}

.agent-description {

    color:
        #64748b;

    font-size:
        11px;

    line-height:
        1.55;

    margin-top:
        9px;
}


/* =====================================================
   ALERTS
   ===================================================== */

div[data-testid="stAlert"] {

    border-radius:
        16px;

    border:
        1px solid
        rgba(148, 163, 184, 0.15);

    animation:
        fadeInUp 0.4s ease both;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {

    text-align:
        center;

    color:
        #475569;

    font-size:
        11px;

    padding:
        34px 0 6px;

    letter-spacing:
        0.3px;

    border-top:
        1px solid
        rgba(148, 163, 184, 0.08);

    margin-top:
        20px;
}

</style>
""")


# =========================================================
# BENGALURU LOCATIONS
# =========================================================

locations = sorted([

    "Kempegowda International Airport",
    "Yelahanka",
    "Yelahanka New Town",
    "Jakkur",
    "Kogilu",
    "Bagalur",
    "Sahakara Nagar",
    "Amruthahalli",
    "Hebbal",
    "Nagawara",
    "Manyata Tech Park",
    "Thanisandra",
    "HBR Layout",
    "Hennur",
    "Kalyan Nagar",
    "Banaswadi",
    "Horamavu",
    "Ramamurthy Nagar",
    "Kammanahalli",

    "Majestic",
    "KSR Bengaluru City Railway Station",
    "KR Market",
    "Gandhinagar",
    "Seshadripuram",
    "Shivajinagar",
    "Vasanth Nagar",
    "Richmond Town",
    "Shanti Nagar",
    "Wilson Garden",
    "Ulsoor",
    "Halasuru",
    "Frazer Town",
    "MG Road",
    "Brigade Road",
    "Commercial Street",
    "Cubbon Park",

    "Malleshwaram",
    "Sadashivanagar",
    "Rajajinagar",
    "Basaveshwaranagar",
    "Vijayanagar",
    "Nagarbhavi",
    "Nandini Layout",
    "Mahalakshmi Layout",
    "Peenya",
    "Jalahalli",
    "Dasarahalli",
    "Tumkur Road",
    "Nayandahalli",
    "Mysore Road",
    "Kengeri",
    "Rajarajeshwari Nagar",

    "Indiranagar",
    "Domlur",
    "HAL",
    "CV Raman Nagar",
    "Kaggadasapura",
    "Vignan Nagar",
    "Baiyappanahalli",
    "KR Puram",
    "Mahadevapura",
    "Hoodi",
    "Doddanekkundi",
    "Marathahalli",
    "AECS Layout",
    "Brookefield",
    "Kundalahalli",
    "ITPL",
    "Whitefield",
    "Hope Farm",
    "Kadugodi",
    "Varthur",
    "Gunjur",
    "Bellandur",
    "Kadubeesanahalli",
    "Panathur",

    "Koramangala",
    "HSR Layout",
    "Bommanahalli",
    "Hongasandra",
    "Singasandra",
    "Kudlu",
    "Begur",
    "Akshayanagar",
    "Arekere",
    "Hulimavu",
    "Bannerghatta Road",
    "Gottigere",
    "Electronic City",
    "Electronic City Phase 1",
    "Electronic City Phase 2",
    "Bommasandra",
    "Hosur Road",

    "BTM Layout",
    "Madivala",
    "Tavarekere",
    "Jayanagar",
    "JP Nagar",
    "Banashankari",
    "Padmanabhanagar",
    "Kumaraswamy Layout",
    "Uttarahalli",
    "Subramanyapura",
    "Konanakunte",
    "Kanakapura Road",
    "Basavanagudi",
    "Gavipuram",
    "Hanumanthanagar",
    "Chamarajpet"

], key=lambda x: x.lower())


# =========================================================
# CONSTANTS
# =========================================================

CITY = "Bengaluru, Karnataka, India"

CAR_MILEAGE = 15

PETROL_PRICE = 100

SAFETY_BUFFER_MINUTES = 10


# =========================================================
# NOMINATIM - LOCATION SEARCH
# =========================================================

@st.cache_data(ttl=86400)
def geocode_location(location):

    url = (
        "https://nominatim.openstreetmap.org/search"
    )

    params = {

        "q":
            f"{location}, Bengaluru, "
            "Karnataka, India",

        "format":
            "json",

        "limit":
            1
    }

    headers = {

        "User-Agent":
            "BengaluruAIUrbanAgent/1.0"
    }

    try:

        response = requests.get(

            url,

            params=params,

            headers=headers,

            timeout=10
        )

        response.raise_for_status()

        results = response.json()

        if not results:

            return None

        return {

            "latitude":
                float(results[0]["lat"]),

            "longitude":
                float(results[0]["lon"]),

            "display_name":
                results[0]["display_name"]
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# OSRM - ROUTE CALCULATION
# =========================================================

def calculate_route(
    origin_lat,
    origin_lon,
    dest_lat,
    dest_lon
):

    url = (

        "https://router.project-osrm.org/"
        "route/v1/driving/"
        f"{origin_lon},{origin_lat};"
        f"{dest_lon},{dest_lat}"
    )

    params = {

        "overview":
            "false",

        "steps":
            "false"
    }

    try:

        response = requests.get(

            url,

            params=params,

            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":

            return None

        route = data["routes"][0]

        return {

            "distance_km":
                route["distance"] / 1000,

            "duration_minutes":
                route["duration"] / 60
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# COST CALCULATION
# =========================================================

def calculate_fuel_cost(
    distance_km,
    mileage,
    petrol_price
):

    if distance_km <= 0:
        return 0

    if mileage <= 0:
        return 0

    fuel_needed = (
        distance_km /
        mileage
    )

    return round(
        fuel_needed *
        petrol_price
    )


# =========================================================
# WEATHER DESCRIPTION
# =========================================================

def weather_description(
    weather_code
):

    descriptions = {

        0:
            "Clear sky",

        1:
            "Mainly clear",

        2:
            "Partly cloudy",

        3:
            "Overcast",

        45:
            "Fog",

        48:
            "Depositing rime fog",

        51:
            "Light drizzle",

        53:
            "Moderate drizzle",

        55:
            "Dense drizzle",

        61:
            "Light rain",

        63:
            "Moderate rain",

        65:
            "Heavy rain",

        71:
            "Light snowfall",

        73:
            "Moderate snowfall",

        75:
            "Heavy snowfall",

        80:
            "Light rain showers",

        81:
            "Moderate rain showers",

        82:
            "Heavy rain showers",

        95:
            "Thunderstorm",

        96:
            "Thunderstorm with hail",

        99:
            "Heavy thunderstorm"
    }

    return descriptions.get(
        weather_code,
        "Weather condition"
    )


# =========================================================
# HERO HEADER
# =========================================================

render_html("""
<div class="hero">

    <div class="hero-small">
        BENGALURU MOBILITY INTELLIGENCE
    </div>

    <div class="hero-title">
        🏙️ Bengaluru AI Urban Decision Agent
    </div>

    <div class="hero-description">
        Intelligent journey planning for Bengaluru using
        geospatial routing, machine learning, traffic
        intelligence, weather intelligence and AI-driven
        decision making.
    </div>

    <div class="online-pill">
        ● SYSTEM ONLINE &nbsp; | &nbsp; AI MVP
    </div>

</div>
""")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## ⚙️ Journey Settings"
    )

    st.caption(
        "Configure your travel preferences."
    )

    travel_mode = st.selectbox(

        "🚗 Travel Mode",

        [
            "Car",
            "Bike",
            "Cab",
            "Public Transport",
            "Metro",
            "Walk"
        ]
    )

    budget = st.number_input(

        "💰 Maximum Budget (₹)",

        min_value=0,

        max_value=10000,

        value=500,

        step=50
    )

    arrival_time = st.time_input(

        "🎯 Required Arrival Time",

        value=time(19, 0)
    )

    st.divider()

    st.markdown(
        "### 🚘 Vehicle Settings"
    )

    mileage = st.number_input(

        "Vehicle Mileage (km/l)",

        min_value=5.0,

        max_value=50.0,

        value=float(
            CAR_MILEAGE
        ),

        step=0.5
    )

    petrol_price = st.number_input(

        "Petrol Price (₹/litre)",

        min_value=50.0,

        max_value=200.0,

        value=float(
            PETROL_PRICE
        ),

        step=1.0
    )

    st.divider()

    st.success(
        "🟢 Application Online"
    )


# =========================================================
# JOURNEY PLANNER
# =========================================================

render_html("""
<div class="section-title">
    📍 Plan Your Bengaluru Journey
</div>

<div class="section-subtitle">
    Select your starting point, destination and
    required arrival time.
</div>
""")


col1, col2 = st.columns(2)


with col1:

    origin = st.selectbox(

        "Starting Location",

        locations,

        index=locations.index(
            "Yelahanka"
        )
    )


with col2:

    destination = st.selectbox(

        "Destination",

        locations,

        index=locations.index(
            "Whitefield"
        )
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze = st.button(

    "🚀  ANALYZE MY JOURNEY",

    type="primary",

    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    # =====================================================
    # VALIDATE
    # =====================================================

    if origin == destination:

        st.error(
            "Starting location and destination "
            "cannot be the same."
        )

        st.stop()


    # =====================================================
    # GEOCODING
    # =====================================================

    with st.spinner(
        "📍 Finding your locations..."
    ):

        origin_data = (
            geocode_location(
                origin
            )
        )

        destination_data = (
            geocode_location(
                destination
            )
        )


    if (
        not origin_data
        or "error" in origin_data
    ):

        st.error(
            f"Could not find the starting location: "
            f"{origin}"
        )

        st.stop()


    if (
        not destination_data
        or "error" in destination_data
    ):

        st.error(
            f"Could not find the destination: "
            f"{destination}"
        )

        st.stop()


    # =====================================================
    # ROUTE
    # =====================================================

    with st.spinner(
        "🛣️ Calculating your route..."
    ):

        route = calculate_route(

            origin_data["latitude"],
            origin_data["longitude"],

            destination_data["latitude"],
            destination_data["longitude"]
        )


    if (
        not route
        or "error" in route
    ):

        st.error(
            "Unable to calculate the route right now."
        )

        st.stop()


    # =====================================================
    # ROUTE VALUES
    # =====================================================

    distance_km = route[
        "distance_km"
    ]

    route_minutes = route[
        "duration_minutes"
    ]


    # =====================================================
    # INITIAL DEPARTURE
    # =====================================================

    today = datetime.today().date()

    arrival_datetime = datetime.combine(

        today,

        arrival_time
    )

    initial_departure = (
        arrival_datetime
        -
        timedelta(
            minutes=
            route_minutes
            +
            SAFETY_BUFFER_MINUTES
        )
    )


    # =====================================================
    # WEATHER AGENT
    # =====================================================

    with st.spinner(
        "🌦️ Checking current weather..."
    ):

        weather_data = get_weather(

            destination_data[
                "latitude"
            ],

            destination_data[
                "longitude"
            ]
        )


    weather_available = (

        weather_data
        and
        "error" not in weather_data
    )


    # =====================================================
    # ML PREDICTION
    # =====================================================

    ml_prediction = None

    try:

        ml_prediction = (
            predict_travel_time(

                distance_km=
                    distance_km,

                baseline_minutes=
                    route_minutes,

                hour=
                    initial_departure.hour,

                day_of_week=
                    initial_departure.weekday()
            )
        )

        if ml_prediction is not None:

            ml_prediction = float(
                ml_prediction
            )

    except Exception:

        ml_prediction = None


    # =====================================================
    # DECISION AGENT
    # =====================================================

    with st.spinner(
        "🧠 AI Decision Agent is analyzing "
        "traffic, weather and ML predictions..."
    ):

        try:

            decision = (
                make_journey_decision(

                    distance_km=
                        distance_km,

                    baseline_minutes=
                        route_minutes,

                    arrival_time=
                        arrival_time,

                    hour=
                        initial_departure.hour,

                    day_of_week=
                        initial_departure.weekday(),

                    ml_prediction=
                        ml_prediction,

                    weather_data=
                        weather_data,

                    safety_buffer=
                        SAFETY_BUFFER_MINUTES
                )
            )

        except Exception as e:

            st.error(
                f"Decision Agent error: {str(e)}"
            )

            st.stop()


    # =====================================================
    # FINAL DECISION VALUES
    # =====================================================

    predicted_minutes = float(
        decision[
            "final_minutes"
        ]
    )

    departure_time = decision[
        "recommended_departure"
    ]

    traffic_level = decision[
        "traffic_level"
    ]

    traffic_multiplier = float(
        decision[
            "traffic_multiplier"
        ]
    )

    traffic_estimated_minutes = float(
        decision[
            "traffic_estimated_minutes"
        ]
    )

    prediction_source = decision[
        "prediction_source"
    ]

    decision_explanation = decision[
        "explanation"
    ]

    weather_level = decision.get(
        "weather_level",
        "Unavailable"
    )

    weather_multiplier = float(
        decision.get(
            "weather_multiplier",
            1.0
        )
    )

    weather_extra_minutes = float(
        decision.get(
            "weather_extra_minutes",
            0
        )
    )


    # =====================================================
    # COST CALCULATION
    # =====================================================

    estimated_cost = 0

    cost_label = "Estimated Cost"


    if travel_mode == "Car":

        estimated_cost = (
            calculate_fuel_cost(

                distance_km,

                mileage,

                petrol_price
            )
        )

        cost_label = (
            "Estimated Fuel Cost"
        )


    elif travel_mode == "Bike":

        estimated_cost = (
            calculate_fuel_cost(

                distance_km,

                40,

                petrol_price
            )
        )

        cost_label = (
            "Estimated Fuel Cost"
        )


    elif travel_mode == "Cab":

        estimated_cost = round(
            50 +
            (
                distance_km *
                18
            )
        )

        cost_label = (
            "Estimated Cab Fare"
        )


    elif travel_mode == "Metro":

        estimated_cost = max(

            20,

            min(
                60,
                round(
                    distance_km * 2
                )
            )
        )

        cost_label = (
            "Estimated Metro Fare"
        )


    elif travel_mode == "Public Transport":

        estimated_cost = max(

            15,

            min(
                50,
                round(
                    distance_km * 1.5
                )
            )
        )

        cost_label = (
            "Estimated Public Transport Fare"
        )


    elif travel_mode == "Walk":

        estimated_cost = 0

        cost_label = (
            "Estimated Cost"
        )


    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    render_html(f"""
<div class="ai-card">

    <div class="ai-label">
        🤖 AI JOURNEY RECOMMENDATION
    </div>

    <div class="ai-time">
        Leave by {departure_time.strftime("%I:%M %p")}
    </div>

    <div class="ai-text">
        Recommended departure from
        <b>{origin}</b> to
        <b>{destination}</b> to reach your destination by
        <b>{arrival_time.strftime("%I:%M %p")}</b>.

        The AI decision combines route distance,
        traffic intelligence, ML prediction and
        current weather conditions.

        A {SAFETY_BUFFER_MINUTES}-minute safety buffer
        is included.
    </div>

</div>
""")


    # =====================================================
    # JOURNEY INTELLIGENCE
    # =====================================================

    render_html("""
<div class="section-title">
    🧭 Journey Intelligence
</div>

<div class="section-subtitle">
    Key information calculated for your journey.
</div>
""")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(

            "🚀 Leave By",

            departure_time.strftime(
                "%I:%M %p"
            )
        )


    with c2:

        st.metric(

            "🏁 Arrival",

            arrival_time.strftime(
                "%I:%M %p"
            )
        )


    with c3:

        st.metric(

            "⏱️ Final Travel Time",

            f"{round(predicted_minutes)} min"
        )


    with c4:

        st.metric(

            "🛡️ Safety Buffer",

            f"{SAFETY_BUFFER_MINUTES} min"
        )


    # =====================================================
    # WEATHER INTELLIGENCE
    # =====================================================

    render_html("""
<div class="section-title">
    🌦️ Weather Intelligence
</div>

<div class="section-subtitle">
    Current weather conditions at your destination.
    Weather conditions are incorporated into the AI
    travel-time decision.
</div>
""")


    if weather_available:

        temperature = weather_data.get(
            "temperature"
        )

        humidity = weather_data.get(
            "humidity"
        )

        apparent_temperature = (
            weather_data.get(
                "apparent_temperature"
            )
        )

        rain = weather_data.get(
            "rain"
        )

        precipitation = weather_data.get(
            "precipitation"
        )

        wind_speed = weather_data.get(
            "wind_speed"
        )

        weather_code = weather_data.get(
            "weather_code"
        )

        description = (
            weather_description(
                weather_code
            )
        )


        w1, w2, w3, w4 = st.columns(4)


        with w1:

            render_html(f"""
<div class="weather-card">

    <div class="weather-label">
        🌡️ Temperature
    </div>

    <div class="weather-value">
        {temperature} °C
    </div>

    <div class="weather-description">
        Feels like {apparent_temperature} °C
    </div>

</div>
""")


        with w2:

            render_html(f"""
<div class="weather-card">

    <div class="weather-label">
        💧 Humidity
    </div>

    <div class="weather-value">
        {humidity}%
    </div>

    <div class="weather-description">
        Current relative humidity
    </div>

</div>
""")


        with w3:

            render_html(f"""
<div class="weather-card">

    <div class="weather-label">
        🌧️ Rain
    </div>

    <div class="weather-value">
        {rain} mm
    </div>

    <div class="weather-description">
        {description}
    </div>

</div>
""")


        with w4:

            render_html(f"""
<div class="weather-card">

    <div class="weather-label">
        💨 Wind
    </div>

    <div class="weather-value">
        {wind_speed} km/h
    </div>

    <div class="weather-description">
        Precipitation: {precipitation} mm
    </div>

</div>
""")


        st.info(

            f"🌦️ Weather impact: "
            f"**{weather_level}** • "
            f"Travel-time multiplier: "
            f"**{weather_multiplier:.2f}x** • "
            f"Estimated additional time: "
            f"**{round(weather_extra_minutes)} min**"
        )

    else:

        st.warning(
            "🌦️ Weather information is currently "
            "unavailable. The Decision Agent continues "
            "using traffic intelligence and ML."
        )


    # =====================================================
    # DISTANCE & COST
    # =====================================================

    render_html("""
<div class="section-title">
    💰 Distance & Estimated Cost
</div>

<div class="section-subtitle">
    Estimated journey distance and travel expense.
</div>
""")


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(

            "📍 Distance",

            f"{distance_km:.1f} km"
        )


    with c2:

        st.metric(

            f"⛽ {cost_label}",

            f"₹{estimated_cost}"
        )


    with c3:

        st.metric(

            "🚗 Travel Mode",

            travel_mode
        )


    # =====================================================
    # BUDGET STATUS
    # =====================================================

    if (
        travel_mode != "Walk"
        and
        estimated_cost > budget
    ):

        st.warning(

            f"⚠️ Estimated cost of "
            f"₹{estimated_cost} exceeds "
            f"your budget of ₹{budget}."
        )

    elif travel_mode != "Walk":

        st.success(

            f"✅ Estimated cost of "
            f"₹{estimated_cost} is within "
            f"your ₹{budget} budget."
        )


    # =====================================================
    # LOCATION INFORMATION
    # =====================================================

    render_html("""
<div class="section-title">
    📍 Journey Locations
</div>

<div class="section-subtitle">
    Resolved geographic locations used by the
    routing and weather engines.
</div>
""")


    c1, c2 = st.columns(2)


    with c1:

        render_html(f"""
<div class="location-card">

    <div class="location-label">
        STARTING POINT
    </div>

    <div class="location-name">
        📍 {origin}
    </div>

    <div class="location-description">
        {origin_data["display_name"]}
    </div>

</div>
""")


    with c2:

        render_html(f"""
<div class="location-card">

    <div class="location-label">
        DESTINATION
    </div>

    <div class="location-name">
        🏁 {destination}
    </div>

    <div class="location-description">
        {destination_data["display_name"]}
    </div>

</div>
""")


    # =====================================================
    # AI AGENT PIPELINE
    # =====================================================

    render_html("""
<div class="section-title">
    🧠 AI Agent Pipeline
</div>

<div class="section-subtitle">
    Modular intelligence components contributing
    to the final journey decision.
</div>
""")


    a1, a2, a3, a4, a5 = st.columns(5)


    # -----------------------------------------------------
    # LOCATION AGENT
    # -----------------------------------------------------

    with a1:

        render_html("""
<div class="agent-card">

    <div class="agent-title">
        📍 Location Agent
    </div>

    <div class="agent-online">
        ● ACTIVE
    </div>

    <div class="agent-description">
        Resolves Bengaluru locations and geographic
        coordinates using Nominatim.
    </div>

</div>
""")


    # -----------------------------------------------------
    # ROUTE AGENT
    # -----------------------------------------------------

    with a2:

        render_html("""
<div class="agent-card">

    <div class="agent-title">
        🛣️ Route Agent
    </div>

    <div class="agent-online">
        ● ACTIVE
    </div>

    <div class="agent-description">
        Calculates route distance and baseline
        travel duration using OSRM.
    </div>

</div>
""")


    # -----------------------------------------------------
    # ML AGENT
    # -----------------------------------------------------

    with a3:

        if ml_prediction is not None:

            ml_status = "● ACTIVE"

            ml_class = (
                "agent-online"
            )

            ml_description = (
                "Machine learning model predicts "
                "journey duration."
            )

        else:

            ml_status = "● FALLBACK"

            ml_class = (
                "agent-next"
            )

            ml_description = (
                "ML prediction unavailable; "
                "system uses traffic intelligence."
            )


        render_html(f"""
<div class="agent-card">

    <div class="agent-title">
        🤖 ML Prediction Agent
    </div>

    <div class="{ml_class}">
        {ml_status}
    </div>

    <div class="agent-description">
        {ml_description}
    </div>

</div>
""")


    # -----------------------------------------------------
    # TRAFFIC AGENT
    # -----------------------------------------------------

    with a4:

        render_html(f"""
<div class="agent-card">

    <div class="agent-title">
        🚦 Traffic Agent
    </div>

    <div class="agent-online">
        ● ACTIVE
    </div>

    <div class="agent-description">

        Traffic:
        <b>{traffic_level}</b>

        <br>

        Multiplier:
        <b>{traffic_multiplier:.2f}x</b>

        <br>

        Estimated:
        <b>{round(traffic_estimated_minutes)} min</b>

    </div>

</div>
""")


    # -----------------------------------------------------
    # WEATHER AGENT
    # -----------------------------------------------------

    with a5:

        if weather_available:

            weather_status = (
                "● ACTIVE"
            )

            weather_class = (
                "agent-online"
            )

            weather_agent_description = (

                f"Current condition: "
                f"{weather_level}. "
                f"Impact: "
                f"{weather_multiplier:.2f}x."
            )

        else:

            weather_status = (
                "● FALLBACK"
            )

            weather_class = (
                "agent-next"
            )

            weather_agent_description = (
                "Weather data unavailable. "
                "Decision continues without weather impact."
            )


        render_html(f"""
<div class="agent-card">

    <div class="agent-title">
        🌦️ Weather Agent
    </div>

    <div class="{weather_class}">
        {weather_status}
    </div>

    <div class="agent-description">
        {weather_agent_description}
    </div>

</div>
""")


    # =====================================================
    # DECISION AGENT
    # =====================================================

    render_html("""
<div class="section-title">
    🤖 Decision Agent
</div>

<div class="section-subtitle">
    Final journey decision produced by combining
    routing, traffic intelligence, ML prediction
    and weather intelligence.
</div>
""")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(

            "🚦 Traffic Estimate",

            f"{round(traffic_estimated_minutes)} min"
        )


    with c2:

        if ml_prediction is not None:

            st.metric(

                "🤖 ML Prediction",

                f"{round(ml_prediction)} min"
            )

        else:

            st.metric(

                "🤖 ML Prediction",

                "Unavailable"
            )


    with c3:

        st.metric(

            "🌦️ Weather Impact",

            f"{weather_multiplier:.2f}x"
        )


    with c4:

        st.metric(

            "🧠 Final Decision",

            f"{round(predicted_minutes)} min"
        )


    # =====================================================
    # DECISION EXPLANATION
    # =====================================================

    render_html("""
<div class="section-title">
    🧠 Decision Explanation
</div>

<div class="section-subtitle">
    Why the system selected this departure time.
</div>
""")


    st.info(

        f"To reach **{destination}** by "
        f"**{arrival_time.strftime('%I:%M %p')}**, "
        f"the Decision Agent recommends leaving at "
        f"**{departure_time.strftime('%I:%M %p')}**. "

        f"The calculated route distance is approximately "
        f"**{distance_km:.1f} km** and the final estimated "
        f"travel time is **{round(predicted_minutes)} minutes**. "

        f"Traffic condition: **{traffic_level}**. "

        f"Weather condition: **{weather_level}**. "

        f"A **{SAFETY_BUFFER_MINUTES}-minute safety buffer** "
        f"is included. "

        f"Prediction source: **{prediction_source}**. "

        f"{decision_explanation}"
    )


    # =====================================================
    # TECHNICAL STATUS
    # =====================================================

    render_html("""
<div class="section-title">
    ⚙️ System Status
</div>
""")


    ml_status_text = (
        "🟢 ML prediction available"
        if ml_prediction is not None
        else
        "🟡 ML prediction unavailable"
    )


    weather_status_text = (
        "🟢 Weather intelligence active"
        if weather_available
        else
        "🟡 Weather intelligence unavailable"
    )


    st.success(

        "🟢 Routing engine online • "
        f"{ml_status_text} • "
        "🟢 Traffic intelligence active • "
        f"{weather_status_text} • "
        "🟢 Decision agent active"
    )


else:

    # =====================================================
    # EMPTY STATE
    # =====================================================

    render_html("""
<div class="ai-card">

    <div class="ai-label">
        🤖 READY
    </div>

    <div class="ai-time">
        Plan your journey
    </div>

    <div class="ai-text">

        Choose your starting location, destination
        and required arrival time.

        The AI system will calculate the route,
        estimate travel duration, analyze traffic,
        check current weather and recommend when
        you should leave.

    </div>

</div>
""")


# =========================================================
# FOOTER
# =========================================================

render_html("""
<div class="footer">

    🏙️ Bengaluru AI Urban Decision Agent

    &nbsp; • &nbsp;

    AI-powered mobility prototype

    &nbsp; • &nbsp;

    OpenStreetMap + Nominatim + OSRM

    &nbsp; • &nbsp;

    ML + Traffic Agent + Weather Agent

    &nbsp; • &nbsp;

    Decision Agent

</div>
""")