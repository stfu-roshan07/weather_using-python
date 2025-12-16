from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import requests

# OpenWeatherMap API details (replace with your API key)
API_KEY = "your_api_key_here"  # Get from https://openweathermap.org/api
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

print("Starting Weather App...")  # Debug print

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

# Function to safely load images (avoids crashes if files missing)
def load_image(filename):
    try:
        return PhotoImage(file=filename)
    except Exception as e:
        print(f"Error loading {filename}: {e}. Using placeholder.")
        return None  # Or create a blank image if needed

# Search box
Search_image = load_image("search.png")
if Search_image:
    myimage = Label(image=Search_image)
    myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#1B1A1A", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

search_icon = load_image("search_icon.png")
if search_icon:
    myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", command=lambda: get_weather())
    myimage_icon.place(x=400, y=34)

# Logo
Logo_image = load_image("logo.png")
if Logo_image:
    logo = Label(image=Logo_image)
    logo.place(x=150, y=100)

# Box image
Box_image = load_image("box.png")
if Box_image:
    box = Label(image=Box_image)
    box.place(x=30, y=400)

# Frame for weather info
frame = Frame(root, width=900, height=180, bg="#1ab5ef")
frame.pack(side=BOTTOM)

# Time label
time_label = Label(root, font=("Arial", 20), fg="#fff", bg="#1ab5ef")
time_label.place(x=30, y=100)

# Labels for weather data
label1 = Label(frame, font=("Arial", 15, 'bold'), bg="#1ab5ef")
label1.place(x=30, y=20)

label2 = Label(frame, font=("Arial", 12), bg="#1ab5ef")
label2.place(x=30, y=50)

label3 = Label(frame, font=("Arial", 10), bg="#1ab5ef")
label3.place(x=30, y=80)

label4 = Label(frame, font=("Arial", 10), bg="#1ab5ef")
label4.place(x=30, y=110)

# Function to get weather data
def get_weather():
    print("Fetching weather...")  # Debug print
    city = textfield.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name.")
        return
    
    try:
        # Geocode the city
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        if not location:
            messagebox.showerror("Error", "City not found.")
            return
        
        lat, lng = location.latitude, location.longitude
        
        # Get timezone
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=lng, lat=lat)
        if not timezone_str:
            timezone_str = "UTC"
        
        # Fetch weather data
        params = {"lat": lat, "lon": lng, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code != 200:
            messagebox.showerror("Error", f"API Error: {data.get('message', 'Unknown error')}")
            return
        
        # Extract and display weather info
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"].capitalize()
        
        label1.config(text=f"{temp}°C | {description}")
        label2.config(text=f"Feels Like: {feels_like}°C | Humidity: {humidity}%")
        label3.config(text=f"Pressure: {pressure} hPa | Wind Speed: {wind_speed} m/s")
        label4.config(text=f"Timezone: {timezone_str}")
        
        # Update time
        tz = pytz.timezone(timezone_str)
        current_time = datetime.now(tz).strftime("%I:%M %p")
        time_label.config(text=current_time)
        
        print("Weather updated successfully.")  # Debug print
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network error: {e}")
        print(f"Network error: {e}")  # Debug print
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        print(f"General error: {e}")  # Debug print

print("GUI initialized. Running mainloop...")  # Debug print
root.mainloop()