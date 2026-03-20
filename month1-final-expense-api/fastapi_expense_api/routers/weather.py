"""Weather API endpoint using Open-Meteo."""

import requests
from fastapi import APIRouter, HTTPException
from fastapi_expense_api.models import WeatherResponse

router = APIRouter(prefix="/weather", tags=["weather"])

# Open-Meteo API endpoints
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Weather code descriptions (Open-Meteo WMO codes)
WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather_description(code: int) -> str:
    """Get human-readable weather description from Open-Meteo code.

    Args:
        code: WMO weather code

    Returns:
        Human-readable description
    """
    return WEATHER_DESCRIPTIONS.get(code, f"Unknown (code {code})")


@router.get("/{city}", response_model=WeatherResponse)
def get_weather(city: str):
    """Get current weather for a city.

    Args:
        city: Name of the city to look up

    Returns:
        WeatherResponse with temperature, weather code, and description

    Raises:
        HTTPException: If city not found or API call fails
    """
    # Step 1: Geocoding - convert city name to coordinates
    try:
        geo_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Geocoding API error: {str(e)}")

    if "results" not in geo_data or not geo_data["results"]:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")

    location = geo_data["results"][0]
    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]

    # Step 2: Weather - fetch current weather using coordinates
    try:
        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True,
            },
            timeout=10,
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Weather API error: {str(e)}")

    if "current_weather" not in weather_data:
        raise HTTPException(status_code=502, detail="Invalid weather API response")

    current = weather_data["current_weather"]
    weather_code = current["weathercode"]
    temperature = current["temperature"]

    return WeatherResponse(
        city=city_name,
        temperature=temperature,
        weather_code=weather_code,
        description=get_weather_description(weather_code),
    )
