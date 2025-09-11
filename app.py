import streamlit as st
import json
from utils.weather_api import get_weather
import os

st.set_page_config(page_title="Weather App", page_icon="🌦️", layout="centered")

with open("static/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Weather App")

FAV_FILE = "favorites.json"

def load_favorites():
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r") as f:
            return json.load(f)
    return []

def save_favorites(fav_list):
    with open(FAV_FILE, "w") as f:
        json.dump(fav_list, f)


if "favorites" not in st.session_state:
    st.session_state["favorites"] = load_favorites()

tab1, tab2, tab3 = st.tabs(["Single City", "Compare Cities", "Favorites"])

with tab1:
    city = st.text_input("Enter a city name:")
    if st.button("Get Weather"):
        if city:
            weather = get_weather(city)
            if "error" in weather:
                st.error(weather["error"])
            else:
                st.session_state["last_weather"] = weather
                st.markdown(f"""
                <div class="card">
                    <div class="weather-header">{weather['city']}</div>
                    🌡️ Temperature: {weather['temperature']} °C  
                    💧 Humidity: {weather['humidity']}%  
                    🌥️ Condition: {weather['condition']}
                </div>
                """, unsafe_allow_html=True)

    if "last_weather" in st.session_state:
        if st.button("Add to Favorites"):
            city_to_save = st.session_state["last_weather"]["city"]
            if city_to_save not in st.session_state["favorites"]:
                st.session_state["favorites"].append(city_to_save)
                save_favorites(st.session_state["favorites"])
                st.success(f"{city_to_save} saved to favorites!")
            else:
                st.warning(f"{city_to_save} is already in favorites.")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        city1 = st.text_input("City 1")
    with col2:
        city2 = st.text_input("City 2")

    if st.button("Compare"):
        if city1 and city2:
            w1, w2 = get_weather(city1), get_weather(city2)
            col1, col2 = st.columns(2)
            for col, w in zip([col1, col2], [w1, w2]):
                with col:
                    if "error" in w:
                        st.error(w["error"])
                    else:
                        st.markdown(f"""
                        <div class="card">
                            <div class="weather-header">{w['city']}</div>
                            🌡️ {w['temperature']} °C  
                            💧 {w['humidity']}%  
                            🌥️ {w['condition']}
                        </div>
                        """, unsafe_allow_html=True)

with tab3:
    st.subheader("⭐ Favorite Cities")
    favorites_copy = st.session_state["favorites"][:]

    if favorites_copy:
        for fav in favorites_copy:
            weather = get_weather(fav)
            if "error" not in weather:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <div class="weather-header">{weather['city']}</div>
                        🌡️ {weather['temperature']} °C  
                        💧 {weather['humidity']}%  
                        🌥️ {weather['condition']}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Remove", key=f"remove_{fav}"):
                        st.session_state["favorites"].remove(fav)
                        save_favorites(st.session_state["favorites"])
                        st.session_state["dummy"] = st.session_state.get("dummy", 0) + 1
                        st.experimental_rerun = None
                        st.experimental_rerun = lambda: None
                        st.experimental_rerun()
    else:
        st.info("No favorites saved yet. Add some from the Single City tab.")
