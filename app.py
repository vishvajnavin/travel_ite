import streamlit as st
import cohere
from datetime import datetime, timedelta
import os
import requests

# Cohere API Key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")  # Set this in your environment variables

# Initialize Cohere Client
co = cohere.Client(COHERE_API_KEY)

def get_live_places(destination, place_type):
    """Fetches real-time places of interest from Google Places API"""
    API_KEY = "YOUR_GOOGLE_PLACES_API_KEY"  # Replace with your API key
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={place_type}+in+{destination}&key={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    places = [place["name"] for place in data.get("results", [])[:5]]
    return places  # Returns top 5 places

def get_activity_suggestions(destination, interests):
    """Generates detailed itinerary suggestions using Cohere AI"""
    prompt = f"Generate a detailed travel itinerary for {destination}, covering attractions, food spots, and activities based on these interests: {', '.join(interests)}."

    try:
        response = co.generate(
            model="command",  
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.generations[0].text.split("\n")  # Split into list
    except Exception as e:
        st.error(f"Error generating activities: {e}")
        return []

def generate_itinerary(destination, duration, interests):
    """Creates AI-generated itinerary"""
    itinerary = {}
    for day in range(1, duration + 1):
        date = (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
        activities = get_activity_suggestions(destination, interests)
        itinerary[f'Day {day} ({date})'] = {
            "Morning": activities[:2],
            "Afternoon": activities[2:4],
            "Evening": activities[4:]
        }
    return itinerary

# Streamlit UI
st.title("🌍 AI-Powered Travel Planner")

st.sidebar.header("✈️ User Preferences")
budget = st.sidebar.selectbox("💰 Budget", ["Low", "Moderate", "High"])
duration = st.sidebar.slider("📅 Trip Duration (days)", 1, 14, 3)
destination = st.sidebar.text_input("📍 Destination", "Paris")
start_location = st.sidebar.text_input("🚀 Starting Location", "Your City")
purpose = st.sidebar.text_area("🎯 Describe your reason for travel", "I want to explore history and try local food.")

interests = st.sidebar.multiselect("🔍 Select Your Interests", ["Historical", "Nature", "Food", "Adventure"])

if st.sidebar.button("🚀 Generate Itinerary"):
    st.subheader(f"🗺️ AI-Powered Personalized Itinerary for {destination}")

    itinerary = generate_itinerary(destination, duration, interests)
    
    for day, schedule in itinerary.items():
        st.markdown(f"## 📅 {day}")
        for time, activities in schedule.items():
            st.markdown(f"**{time}:**")
            for activity in activities:
                st.write(f"- {activity}")

    st.write("For a comfortable stay, AI suggests **Hotel de Crillon**—budget-friendly & near attractions.")

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ using Streamlit & Cohere AI")