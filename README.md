# 🏙️ Bengaluru AI Urban Decision Agent

> **AI-powered journey decision support for Bengaluru that answers: “When should I leave to reach my destination on time?”**

🌐 **Live Demo:** https://bengaluru-ai-decision-agent-dta8jddrasxpxemgenwumc.streamlit.app/

## 📌 Overview

The **Bengaluru AI Urban Decision Agent** is a Python and Streamlit-based AI/ML application for urban mobility decision support.

Instead of only calculating a route, the application combines:

- Geographic location resolution
- Route distance and baseline travel time
- Traffic intelligence
- Machine-learning travel-time prediction
- A decision agent
- Travel-mode and budget estimation
- A configurable safety buffer

The final output is an **actionable recommended departure time**, together with estimated travel duration, traffic condition, cost, prediction source, and an explanation.

The project is focused on **Bengaluru urban mobility** and is designed as a modular multi-agent/agentic decision-support prototype.

---

## 🎯 Problem Statement

Traditional navigation applications are primarily designed around route navigation and estimated arrival time.

This project approaches the problem from another direction:

> **Given a destination and a required arrival time, when should the user leave?**

```text
Destination + Required Arrival Time
                ↓
             Route
                ↓
      Baseline Travel Time
                ↓
       Traffic Intelligence
                +
          ML Prediction
                ↓
        Decision Agent
                ↓
         Safety Buffer
                ↓
   Recommended Departure Time
```

---

## 🚀 Live Application

**Streamlit Application:**

https://bengaluru-ai-decision-agent-dta8jddrasxpxemgenwumc.streamlit.app/

The application allows users to:

1. Select a Bengaluru starting location.
2. Select a destination.
3. Choose a travel mode.
4. Set a maximum travel budget.
5. Enter the required arrival time.
6. Configure vehicle mileage and petrol price.
7. Analyze the journey.
8. Receive a recommended departure time.

---

## 🧠 Why This Is an Agentic AI / Multi-Agent Project

The project is structured around specialized intelligence components rather than putting all logic into one large function.

| Component | Responsibility |
|---|---|
| Location / Geocoding | Resolves Bengaluru locations into coordinates |
| Route Intelligence | Calculates route distance and baseline duration |
| Traffic Agent | Estimates traffic impact using time/day context |
| Weather Agent | Provides weather-data capability through Open-Meteo |
| ML Prediction Agent | Loads the trained travel-time model and generates a prediction |
| Decision Agent | Combines available intelligence and produces the final journey decision |

The **Decision Agent** is the central reasoning layer. It receives outputs from routing, traffic and ML components and converts them into an actionable recommendation.

> **Implementation note:** The current deployed journey-decision flow primarily uses Location → OSRM Route → Traffic Intelligence + ML Prediction → Decision Agent. The Weather Agent is implemented as a modular capability and can be integrated more deeply into the final decision formula in a future version.

---

## 🏗️ System Architecture

```text
                         ┌───────────────────────┐
                         │       USER INPUT      │
                         │                       │
                         │ Starting Location     │
                         │ Destination           │
                         │ Arrival Time          │
                         │ Travel Mode           │
                         │ Budget                │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    LOCATION AGENT     │
                         │ Nominatim / OSM       │
                         │ Address → Coordinates │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      ROUTE AGENT      │
                         │ OSRM                  │
                         │ Distance              │
                         │ Baseline duration     │
                         └───────────┬───────────┘
                                     │
                  ┌──────────────────┴─────────────────┐
                  ▼                                    ▼
        ┌────────────────────┐              ┌────────────────────┐
        │   TRAFFIC AGENT    │              │   ML AGENT         │
        │ Time of day        │              │ Trained model      │
        │ Day of week        │              │ joblib             │
        │ Traffic multiplier │              │ Travel prediction  │
        └─────────┬──────────┘              └──────────┬─────────┘
                  └────────────────┬───────────────────┘
                                   ▼
                       ┌─────────────────────────┐
                       │     DECISION AGENT      │
                       │ Traffic estimate        │
                       │ ML prediction           │
                       │ Baseline sanity check   │
                       │ Safety buffer            │
                       └────────────┬────────────┘
                                    ▼
                       ┌─────────────────────────┐
                       │    FINAL RECOMMENDATION │
                       │ Leave-by time           │
                       │ Travel duration         │
                       │ Traffic level           │
                       │ Cost                    │
                       │ Explanation             │
                       └─────────────────────────┘
```

---

## 🔄 End-to-End Data Flow

```text
User
 │
 ├── Starting Location
 ├── Destination
 ├── Required Arrival Time
 ├── Travel Mode
 └── Budget
       │
       ▼
Nominatim
       │
       ▼
Coordinates
       │
       ▼
OSRM
       ├── Distance
       └── Baseline Travel Time
                 │
                 ├─────────────────────┐
                 ▼                     ▼
          Traffic Agent           ML Prediction
                 │                     │
                 ▼                     ▼
          Traffic Estimate       ML Estimate
                 │                     │
                 └──────────┬──────────┘
                            ▼
                     Decision Agent
                            │
                            ▼
                  Final Travel Time
                            │
                            ▼
                     Safety Buffer
                            │
                            ▼
                 Recommended Departure
```

---

## 🤖 Decision Agent

Implemented in:

```text
agents/decision_agent.py
```

When an ML prediction is available:

```text
Final Travel Time =
    Traffic Estimate × 60%
    +
    ML Prediction × 40%
```

A sanity check ensures the final estimate does not fall below the baseline route duration.

Then:

```text
Recommended Departure =
Required Arrival Time
- Final Travel Time
- Safety Buffer
```

The default safety buffer is **10 minutes**.

---

## 🚦 Traffic Intelligence

Implemented in:

```text
agents/traffic_agent.py
```

Inputs include:

- Baseline route duration
- Hour of day
- Day of week

Outputs include:

- Traffic level
- Traffic multiplier
- Estimated traffic travel time
- Explanation

---

## 🤖 Machine Learning Component

```text
ml/
├── predict.py
├── train_model.py
├── test_prediction.py
└── travel_time_model.pkl
```

The prediction module loads the trained model using `joblib`.

The prediction pipeline uses journey-related features such as:

```text
Distance
Baseline Travel Duration
Hour
Day of Week
```

The ML estimate is combined with Traffic Intelligence by the Decision Agent.

---

## 🌦️ Weather Agent

Implemented in:

```text
agents/weather_agent.py
```

The Weather Agent uses the **Open-Meteo API** to retrieve current weather information, including:

- Temperature
- Relative humidity
- Apparent temperature
- Precipitation
- Rain
- Weather code
- Wind speed
- Observation time

The agent is separated from the core decision logic so it can be incorporated into a future weather-aware travel model.

---

## 📍 Location Intelligence

The application contains a curated list of Bengaluru locations, including Yelahanka, Jakkur, Hebbal, Manyata Tech Park, Hennur, Majestic, MG Road, Indiranagar, Koramangala, Whitefield, Marathahalli, Bellandur, Electronic City, JP Nagar, Jayanagar, Banashankari, Kengeri, Rajarajeshwari Nagar, Kempegowda International Airport and many other areas.

Selected locations are converted to coordinates using Nominatim.

---

## 🗺️ Route Intelligence

The project uses **OSRM (Open Source Routing Machine)** for route calculation.

```text
Origin coordinates
       +
Destination coordinates
       ↓
OSRM
       ↓
Distance + Baseline Travel Duration
```

The baseline duration becomes the foundation for traffic and ML calculations.

---

## 💰 Travel Cost Estimation

Supported travel modes:

```text
Car
Bike
Cab
Public Transport
Metro
Walk
```

### Car

```text
Fuel required = Distance / Mileage
Fuel cost = Fuel required × Petrol Price
```

### Bike

Uses a default mileage assumption for estimation.

### Cab

Uses a prototype distance-based fare estimate.

### Metro / Public Transport

Uses prototype distance-based fare estimates with limits.

### Walk

```text
Estimated cost = ₹0
```

> These are prototype estimates and are not official fares.

---

## 💵 Budget Intelligence

Users can define a maximum budget.

The application compares:

```text
Estimated Journey Cost
        vs
User Budget
```

and reports whether the estimate is within the selected budget.

---

## 🖥️ User Interface

The Streamlit dashboard includes:

### Hero Dashboard
- Project title
- System status
- AI mobility description

### Journey Planner
- Starting location
- Destination
- Travel mode
- Arrival time
- Budget

### Vehicle Settings
- Mileage
- Petrol price

### AI Recommendation
- Recommended leave-by time
- Destination
- Required arrival time
- Safety buffer

### Journey Intelligence
- Leave-by time
- Required arrival
- Final travel time
- Safety buffer

### Distance & Cost
- Distance
- Estimated cost
- Travel mode

### Journey Locations
- Resolved starting location
- Resolved destination

### AI Agent Pipeline
- Location Agent
- Route Agent
- ML Prediction Agent
- Traffic Intelligence

### Decision Agent
- Traffic estimate
- ML prediction
- Final decision
- Prediction source
- Explanation

---

## 🆚 How Is It Different From Google Maps?

This project is **not intended to replace Google Maps**. Google Maps is a mature navigation platform with extensive mapping, routing, traffic, places and navigation capabilities.

This project has a narrower objective: **decision support for when to leave**.

| Capability | Bengaluru AI Urban Decision Agent | Google Maps |
|---|---|---|
| Route calculation | ✅ | ✅ |
| Distance | ✅ | ✅ |
| ETA | ✅ | ✅ |
| Traffic consideration | ✅ | ✅ |
| Custom ML travel-time model | ✅ | Not exposed to users |
| Explicit Decision Agent | ✅ | Not exposed as a user-facing component |
| Custom safety buffer | ✅ | Different workflow |
| Budget estimation | ✅ | Not the core focus |
| Open-source routing components | ✅ | ❌ |
| Custom Python architecture | ✅ | ❌ |
| Modular agent architecture | ✅ | Not exposed to users |
| Primary objective | **When should I leave?** | **Navigation and route planning** |

### Simple explanation

```text
Google Maps:
"Here is your route. It will take approximately X minutes."

Bengaluru AI Urban Decision Agent:
"You need to arrive by 7:00 PM. Based on the available
route, traffic intelligence, ML estimate and safety buffer,
when should you start your journey?"
```

The core distinction is:

> **Navigation → Decision Intelligence**

---

## 🧠 Why the Project Is More Than an API Wrapper

The application follows a decision pipeline rather than displaying a single external API response:

```text
External Data
     ↓
Specialized Intelligence
     ↓
Prediction / Processing
     ↓
Decision Agent
     ↓
Actionable Recommendation
```

This demonstrates a practical combination of:

- Agentic architecture
- AI decision support
- Machine-learning integration
- API orchestration
- Urban mobility intelligence

---

## 📊 Example Decision

Example scenario:

```text
Origin:             Yelahanka
Destination:        Whitefield
Required Arrival:   7:00 PM
Travel Mode:        Car
```

The application calculates:

```text
Route Distance
      ↓
Baseline Route Time
      ↓
Traffic Estimate
      ↓
ML Prediction
      ↓
Final Travel Time
      ↓
+ Safety Buffer
      ↓
Recommended Departure
```

Exact values change according to the selected locations, arrival time, routing response, traffic logic and ML prediction.

---

## 🔐 Reliability and Fallback Behavior

If ML prediction is available:

```text
Traffic Intelligence + ML Prediction
                ↓
          Combined Decision
```

If ML prediction is unavailable:

```text
Traffic Intelligence
        ↓
   Final Decision
```

The final estimated duration is also constrained so it does not fall below the routing baseline.

---

## 🧪 Testing

The repository contains test modules for individual components:

```text
agents/test_traffic_agent.py
agents/test_weather_agent.py
ml/test_prediction.py
```

These help validate components independently from the Streamlit interface.

---

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

```text
Local VS Code Project
        ↓
GitHub Repository
        ↓
Streamlit Community Cloud
        ↓
requirements.txt
        ↓
Python Environment
        ↓
app.py
        ↓
Live Application
```

**Live Demo:**
https://bengaluru-ai-decision-agent-dta8jddrasxpxemgenwumc.streamlit.app/

---

## 📁 Project Structure

```text
Bengaluru AI Agent/
│
├── agents/
│   ├── __init__.py
│   ├── decision_agent.py
│   ├── traffic_agent.py
│   ├── weather_agent.py
│   ├── test_traffic_agent.py
│   └── test_weather_agent.py
│
├── ml/
│   ├── predict.py
│   ├── train_model.py
│   ├── test_prediction.py
│   └── travel_time_model.pkl
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠️ Technology Stack

### Programming
- Python

### Application
- Streamlit

### Machine Learning
- Scikit-learn / trained ML model
- Joblib
- Pandas

### Geospatial / Routing
- OpenStreetMap
- Nominatim
- OSRM

### Weather
- Open-Meteo API

### HTTP / APIs
- Requests

### Version Control
- GitHub

### Deployment
- Streamlit Community Cloud

---

## 🌐 External Services

### Nominatim / OpenStreetMap
Used for geocoding location names into latitude and longitude.

### OSRM
Used for route distance and baseline driving duration.

### Open-Meteo
Used by the Weather Agent for current weather information.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/dharshivam/bengaluru-ai-urban-decision-agent.git
```

Move into the project directory:

```bash
cd bengaluru-ai-urban-decision-agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application according to the location of `app.py`:

```bash
streamlit run "Bengaluru AI Agent/app.py"
```

or, if `app.py` is at repository root:

```bash
streamlit run app.py
```

---

## ⚠️ Limitations

This is an AI/ML prototype and should not be interpreted as an official traffic or navigation service.

Current limitations include:

- Traffic intelligence is not equivalent to a commercial real-time traffic feed.
- Cost estimates are approximate.
- OSRM does not provide all capabilities of commercial navigation platforms.
- The Weather Agent is implemented separately and is not yet deeply integrated into the final travel-time formula.
- ML accuracy depends on the quality and representativeness of the training data.
- Predictions are estimates, not guarantees.
- The application is currently focused on Bengaluru.

---

## 🚀 Future Enhancements

### 1. Real-Time Traffic API
Integrate live road-condition data into the Traffic Agent.

### 2. Weather-Aware Travel Prediction
Use rainfall, precipitation and other weather features in the ML model.

### 3. Multiple Route Comparison
Compare multiple routes using time, traffic, cost and reliability.

### 4. Personalized Travel Intelligence
Learn user-specific travel patterns, preferred routes, travel modes and budgets.

### 5. Event and Road-Closure Intelligence
Incorporate major Bengaluru events, road closures and construction information.

### 6. LLM Explanation Agent
Generate natural-language explanations for why a departure time was recommended.

### 7. Multi-City Expansion
Extend the architecture to other Indian cities.

---

## 🎓 Skills Demonstrated

### Python
- Modular programming
- Exception handling
- API integration
- Data processing

### Machine Learning
- Model training
- Model persistence
- Feature-based inference
- Prediction pipeline

### AI / Agentic Systems
- Specialized agents
- Decision orchestration
- Agent outputs
- Decision logic

### APIs
- REST API consumption
- Geocoding
- Routing
- Weather services

### Data / Geospatial Intelligence
- Coordinates
- Distance calculation
- Travel duration
- Urban mobility data

### Deployment
- GitHub
- Streamlit
- Cloud deployment
- Dependency management

---

## 🧩 Core Python Modules

### `app.py`
Main Streamlit application responsible for UI, input collection, geocoding, routing, ML invocation, decision-agent invocation, cost calculation and results display.

### `agents/traffic_agent.py`
Traffic intelligence logic.

### `agents/weather_agent.py`
Weather API integration.

### `agents/decision_agent.py`
Central journey decision logic.

### `ml/train_model.py`
ML model training pipeline.

### `ml/predict.py`
Loads the trained model and generates travel-time predictions.

### `ml/travel_time_model.pkl`
Persisted trained ML model.

---

## 🏁 Conclusion

The **Bengaluru AI Urban Decision Agent** demonstrates how machine learning, APIs, geospatial routing and agent-based decision logic can be combined into a practical urban mobility application.

The central idea is:

> **Don't just tell the user how long the journey may take — help the user decide when to start the journey.**

The project provides a foundation for more advanced AI-powered urban mobility and decision-intelligence systems.

---

## 👨‍💻 Author

**Shivam Dhar**  
Bengaluru, India

**Project:** Bengaluru AI Urban Decision Agent  
**Live Demo:** https://bengaluru-ai-decision-agent-dta8jddrasxpxemgenwumc.streamlit.app/  
**GitHub:** https://github.com/dharshivam/bengaluru-ai-urban-decision-agent

---

## ⭐ Project Summary

```text
Project:     Bengaluru AI Urban Decision Agent
Type:        AI / ML / Multi-Agent Decision Support
Domain:      Urban Mobility
Language:    Python
Framework:   Streamlit
ML:          Travel-Time Prediction
Agents:      Location, Route, Traffic, Weather, ML, Decision
Core Output: Recommended Departure Time
Deployment:  Streamlit Community Cloud
```
