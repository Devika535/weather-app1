import requests
import tkinter as tk
from tkinter import messagebox

# --- CONFIGURATION ---
API_KEY = "d4d16dbf69a6c9b360ec51d7216b0166"  # Your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# --- FUNCTIONS ---
def get_weather(city):
    """Fetch weather data from OpenWeatherMap API"""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        # For debugging: print full URL being requested
        url = requests.Request('GET', BASE_URL, params=params).prepare().url
        print(f"Requesting URL: {url}")

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract relevant data
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].title()
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            # Update labels
            result_label.config(
                text=f"📍 {city.title()}\n"
                     f"🌡️ Temp: {temp}°C\n"
                     f"☁️ Weather: {desc}\n"
                     f"💧 Humidity: {humidity}%\n"
                     f"💨 Wind: {wind_speed} m/s"
            )
        else:
            # Show API error message (if any)
            error_message = data.get("message", "City not found.")
            messagebox.showerror("Error", error_message.capitalize())
            result_label.config(text="")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", "Network error occurred.")
        print("Network error:", e)

def on_search():
    city = city_entry.get().strip()
    if city:
        get_weather(city)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")

# --- GUI SETUP ---
app = tk.Tk()
app.title("Weather App")
app.geometry("350x300")
app.resizable(False, False)
app.configure(bg="#e3f2fd")

# Title
title_label = tk.Label(app, text="🌦️ Weather App", font=("Helvetica", 16, "bold"), bg="#e3f2fd")
title_label.pack(pady=10)

# Input Field
city_entry = tk.Entry(app, font=("Helvetica", 12), justify='center')
city_entry.pack(pady=10)
city_entry.focus()

# Search Button
search_button = tk.Button(app, text="Get Weather", font=("Helvetica", 12), command=on_search)
search_button.pack()

# Result Display
result_label = tk.Label(app, text="", font=("Helvetica", 12), justify='left', bg="#e3f2fd")
result_label.pack(pady=20)

# Run the App
app.mainloop()