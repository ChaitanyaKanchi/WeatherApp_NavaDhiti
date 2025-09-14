"""
Weather Application using Streamlit

Features:
- Search weather for a single city
- Compare weather between two cities
- Save favorite cities and view/remove them later
"""

import os
import json
import streamlit as st
from utils.weather_api import get_weather  # Custom weather API utility

# Streamlit Page Configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌦️",
    layout="centered"
)

# Load custom CSS for styling
with open("static/styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Weather App")

# File to store favorites
FAV_FILE = "favorites.json"


def load_favorites():
    """
    Load favorite cities from a JSON file.
    Returns:
        list: List of favorite city names.
    """
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_favorites(fav_list):
    """
    Save favorite cities to a JSON file.
    Args:
        fav_list (list): List of favorite city names.
    """
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(fav_list, f)


# Initialize session state
if "favorites" not in st.session_state:
    st.session_state["favorites"] = load_favorites()

# Tabs for different features
tab1, tab2, tab3 = st.tabs(["Single City", "Compare Cities", "Favorites"])

# Tab 1: Single City Weather
with tab1:
    city = st.text_input("Enter a city name:")

    # Fetch weather for the city
    if st.button("Get Weather"):
        if city:
            weather = get_weather(city)
            if "error" in weather:
                st.error(weather["error"])
            else:
                st.session_state["last_weather"] = weather
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="weather-header">{weather['city']}</div>
                        🌡️ Temperature: {weather['temperature']} °C  
                        💧 Humidity: {weather['humidity']}%  
                        🌥️ Condition: {weather['condition']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Add last searched city to favorites
    if "last_weather" in st.session_state:
        if st.button("Add to Favorites"):
            city_to_save = st.session_state["last_weather"]["city"]
            if city_to_save not in st.session_state["favorites"]:
                st.session_state["favorites"].append(city_to_save)
                save_favorites(st.session_state["favorites"])
                st.success(f"{city_to_save} saved to favorites!")
            else:
                st.warning(f"{city_to_save} is already in favorites.")

# Tab 2: Compare Two Cities
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

            # Display results side by side
            for col, w in zip([col1, col2], [w1, w2]):
                with col:
                    if "error" in w:
                        st.error(w["error"])
                    else:
                        st.markdown(
                            f"""
                            <div class="card">
                                <div class="weather-header">{w['city']}</div>
                                🌡️ {w['temperature']} °C  
                                💧 {w['humidity']}%  
                                🌥️ {w['condition']}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

# Tab 3: Favorite Cities
with tab3:
    st.subheader("⭐ Favorite Cities")
    favorites_copy = st.session_state["favorites"][:]

    if favorites_copy:
        for fav in favorites_copy:
            weather = get_weather(fav)

            if "error" not in weather:
                col1, col2 = st.columns([3, 1])

                # Display favorite city weather
                with col1:
                    st.markdown(
                        f"""
                        <div class="card">
                            <div class="weather-header">{weather['city']}</div>
                            🌡️ {weather['temperature']} °C  
                            💧 {weather['humidity']}%  
                            🌥️ {weather['condition']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Remove city from favorites
                with col2:
                    if st.button("Remove", key=f"remove_{fav}"):
                        st.session_state["favorites"].remove(fav)
                        save_favorites(st.session_state["favorites"])

                        # Force rerun to update UI
                        st.session_state["dummy"] = (
                            st.session_state.get("dummy", 0) + 1
                        )
                        st.experimental_rerun()
    else:
        st.info("No favorites saved yet. Add some from the Single City tab.")