import argparse
import requests
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

# City to coordinates mapping
CITIES = {
    "Beijing": (39.9042, 116.4074),
    "Shanghai": (31.2304, 121.4737),
    "Tokyo": (35.6762, 139.6503),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
}

HISTORY_FILE = "weather_history.json"

console = Console()


def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def save_to_history(city, data):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    current = data.get("current", {})
    record = {
        "city": city,
        "timestamp": datetime.now().isoformat(),
        "temperature_2m": current.get("temperature_2m"),
        "relative_humidity_2m": current.get("relative_humidity_2m"),
        "wind_speed_10m": current.get("wind_speed_10m"),
    }
    history.append(record)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def show_history():
    if not os.path.exists(HISTORY_FILE):
        console.print("[yellow]No history found.[/yellow]")
        return

    with open(HISTORY_FILE, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            console.print("[yellow]No history found.[/yellow]")
            return

    if not history:
        console.print("[yellow]No history found.[/yellow]")
        return

    table = Table(title="Weather History")
    table.add_column("City", style="cyan")
    table.add_column("Time", style="green")
    table.add_column("Temperature (°C)", justify="right")
    table.add_column("Humidity (%)", justify="right")
    table.add_column("Wind Speed (km/h)", justify="right")

    for record in history:
        table.add_row(
            record.get("city", "N/A"),
            record.get("timestamp", "N/A"),
            str(record.get("temperature_2m", "N/A")),
            str(record.get("relative_humidity_2m", "N/A")),
            str(record.get("wind_speed_10m", "N/A")),
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Weather CLI - Get current weather for cities")
    parser.add_argument("city", nargs="?", help="City name (Beijing, Shanghai, Tokyo, New York, London)")
    parser.add_argument("--history", action="store_true", help="Show weather history")

    args = parser.parse_args()

    if args.history:
        show_history()
        return

    if not args.city:
        parser.print_help()
        return

    city_key = args.city.title()
    if city_key not in CITIES:
        console.print(f"[red]City '{args.city}' not found. Available cities:[/red]")
        for city in CITIES:
            console.print(f"  - {city}")
        return

    lat, lon = CITIES[city_key]

    try:
        console.print(f"[cyan]Fetching weather for {city_key}...[/cyan]")
        data = get_weather(lat, lon)
        current = data.get("current", {})

        console.print(f"\n[bold]Weather in {city_key}[/bold]")
        console.print(f"  Temperature: [yellow]{current.get('temperature_2m')}°C[/yellow]")
        console.print(f"  Humidity: [blue]{current.get('relative_humidity_2m')}%[/blue]")
        console.print(f"  Wind Speed: [green]{current.get('wind_speed_10m')} km/h[/green]")

        save_to_history(city_key, data)
        console.print(f"\n[dim]Saved to history.[/dim]")

    except requests.RequestException as e:
        console.print(f"[red]Error fetching weather: {e}[/red]")


if __name__ == "__main__":
    main()
