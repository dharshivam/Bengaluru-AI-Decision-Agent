# Bengaluru AI Urban Decision Agent 🚦🤖

An AI-powered multi-agent system designed to help users decide **when they should leave** to reach their destination on time.

Unlike traditional navigation systems that primarily provide a route and current ETA, this project combines **route intelligence, traffic analysis, weather information, and machine-learning-based travel-time prediction** to generate an intelligent departure-time recommendation.

---

## 🎯 Project Objective

The main objective of this project is to answer:

> **"What time should I leave to reach my destination by my required arrival time?"**

The system analyzes multiple factors that can influence journey duration and produces a recommended departure time with a safety buffer.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │     USER INPUT      │
                         │                     │
                         │ • Current Location  │
                         │ • Destination       │
                         │ • Arrival Time      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │     MULTI-AGENT SYSTEM      │
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────┼─────────────────────────┐
        │                          │                         │
        ▼                          ▼                         ▼
┌────────────────┐        ┌────────────────┐        ┌────────────────┐
│ Location Agent │        │   Route Agent  │        │ Weather Agent  │
│                │        │                │        │                │
│ Address →      │        │ OSRM routing   │        │ Open-Meteo     │
│ Coordinates    │        │ Distance       │        │ Weather data   │
└───────┬────────┘        └───────┬────────┘        └───────┬────────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Traffic Agent   │
                         │                 │
                         │ Traffic level   │
                         │ Multiplier      │
                         │ Estimated time  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ ML Prediction   │
                         │     Agent       │
                         │                 │
                         │ Trained model   │
                         │ Travel-time     │
                         │ prediction      │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │     DECISION AGENT       │
                    │                          │
                    │ Combines:                │
                    │ • Route                  │
                    │ • Traffic                │
                    │ • Weather                │
                    │ • ML prediction          │
                    │ • Safety buffer          │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    FINAL RECOMMENDATION  │
                    │                          │
                    │ Estimated Travel Time    │
                    │ Traffic Level            │
                    │ Recommended Departure    │
                    │ Explanation / Reason     │
                    └──────────────────────────┘
