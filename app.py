import streamlit as st
import requests

# Set page title and icon
st.set_page_config(page_title="AshuWeather", page_icon="🌤️")

def get_weather_desc(code):
    code_map = {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
        45: "Fog 🌫️", 48: "Depositing rime fog 🌁",
        51: "Light drizzle 🌧️", 53: "Moderate drizzle 🌧️", 55: "Dense drizzle 🌧️",
        61: "Slight rain 🌦️", 63: "Moderate rain 🌧️", 65: "Heavy rain ⛈️",
        71: "Slight snow 🌨️", 73: "Moderate snow ❄️", 75: "Heavy snow ⛄",
        80: "Slight rain showers 🌦️", 81: "Moderate rain showers 🌧️", 82: "Violent rain showers ⛈️",
        95: "Thunderstorm 🌩️"
    }
    return code_map.get(code, f"Unknown Code ({code})")

def display_weather_ui(lat, lon, location_name):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        data = requests.get(url, timeout=5).json()
        current = data["current_weather"]
        
        # Displaying the data using Streamlit visual boxes
        st.success(f"### Weather Report for {location_name}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Temperature", value=f"{current['temperature']} °C")
        col2.metric(label="Wind Speed", value=f"{current['windspeed']} km/h")
        col3.metric(label="Condition", value=get_weather_desc(current['weathercode']))
        
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")

# --- WEBSITE LAYOUT ---
st.title("🌤️ AshuWeather")
st.write("Welcome to AshuWeather: Your custom Python-powered dashboard!")

# Navigation sidebar/radio menu
option = st.radio("Choose an action:", ["Auto-detect my location", "Search by city name"])

if option == "Auto-detect my location":
    if st.button("Get Local Weather"):
        with st.spinner("Detecting your location..."):
            try:
                geo_data = requests.get("http://ip-api.com/json/", timeout=5).json()
                if geo_data.get("status") == "success":
                    display_weather_ui(geo_data["lat"], geo_data["lon"], geo_data["city"])
                else:
                    st.error("Could not automatically detect location.")
            except Exception as e:
                st.error(f"Network error: {e}")

elif option == "Search by city name":
    city_input = st.text_input("Enter city name:")
    if st.button("Search"):
        if city_input:
            with st.spinner(f"Searching for '{city_input}'..."):
                try:
                    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_input}&count=1"
                    data = requests.get(url, timeout=5).json()
                    
                    if "results" in data and len(data["results"]) > 0:
                        location = data["results"][0]
                        full_name = f"{location['name']}, {location.get('country', '')}"
                        display_weather_ui(location["latitude"], location["longitude"], full_name)
                    else:
                        st.error("City not found. Please try another name.")
                except Exception as e:
                    st.error(f"Error searching for city: {e}")
        else:
            st.warning("Please type a city name first!")