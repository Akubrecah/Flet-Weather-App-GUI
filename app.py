# modules
import flet
from flet import *
import requests
import json
import os
import datetime
from api_key import API_KEY


API_KEY = API_KEY

# Function to fetch weather data
def fetch_weather_data(city):
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        )
        response.raise_for_status()
        print(f"API Response for {city}:", response.json())  # Debug print
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# New function to fetch weekly forecast data
def fetch_weekly_forecast(city):
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None

# API request with error handling
current = fetch_weather_data("London")
forecast = fetch_weekly_forecast("London")  # New forecast variable

# List of days
days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_weather_details():
    if current is not None:
        try:
            data = current.json()
            if not data:
                print("Empty response from API")
                return None

            weather_data = {
                "description": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"]
            }
            print("Weather details:", weather_data)  # Debug print
            return weather_data

        except (KeyError, TypeError, ValueError) as e:
            print(f"Error parsing weather details: {e}")
            return None
    return None

# New function to get weekly forecast details
def get_weekly_forecast():
    if forecast is None:
        return None
        
    try:
        data = forecast.json()
        if not data or 'list' not in data:
            return None
            
        # Group forecasts by day
        daily_data = {}
        for item in data['list']:
            date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(item)
        
        # Get one forecast per day (midday if possible)
        weekly_forecast = []
        for date, items in daily_data.items():
            # Find forecast closest to 12:00 PM
            midday_forecast = min(items, key=lambda x: abs(12 - int(datetime.datetime.fromtimestamp(x['dt']).strftime('%H'))))
            day_name = datetime.datetime.fromtimestamp(midday_forecast['dt']).strftime('%A')
            weekly_forecast.append({
                'day': day_name,
                'temp': round(midday_forecast['main']['temp']),
                'description': midday_forecast['weather'][0]['description'].capitalize(),
                'icon': midday_forecast['weather'][0]['icon'][:2] + 'd',  # Ensure day icon
                'full_data': midday_forecast  # Store full data for click functionality
            })
        
        return weekly_forecast[:7]  # Return up to 7 days
        
    except Exception as e:
        print(f"Error parsing forecast data: {e}")
        return None


def main(page: Page):
    # Page setup
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.title = "Weather App"

    # Initialize current as a list to make it mutable
    current = [fetch_weather_data("London")]
    forecast = [fetch_weekly_forecast("London")]  # New mutable forecast list

    def update_weather(e):
        if not city_search.value:
            page.show_snack_bar(SnackBar(content=Text("Please enter a city name")))
            return

        new_data = fetch_weather_data(city_search.value)
        new_forecast = fetch_weekly_forecast(city_search.value)  # New forecast fetch
        if new_data and new_forecast:
            current[0] = new_data
            forecast[0] = new_forecast  # Update forecast data
            new_top = top()
            new_forecast_container = weekly_forecast_container()  # New forecast container
            # Update both containers in the column
            c.content.controls[1].content.controls = [new_top, new_forecast_container]
            city_search.value = ""
            page.update()
        else:
            page.show_snack_bar(SnackBar(content=Text("City not found or network error")))

    def update_day_weather(day_data):
        # Create a fake current weather response using the day's forecast data
        fake_current = {
            "weather": [{
                "description": day_data['description'].lower(),
                "icon": day_data['icon']
            }],
            "main": {
                "temp": day_data['temp'],
                "humidity": day_data['full_data']['main']['humidity'],
                "pressure": day_data['full_data']['main']['pressure']
            },
            "wind": {
                "speed": day_data['full_data']['wind']['speed']
            },
            "name": current[0].json()["name"] if current[0] else "Unknown City"
        }
        
        # Update the current weather display
        current[0] = type('obj', (object,), {'json': lambda: fake_current})()
        new_top = top()
        c.content.controls[1].content.controls[0] = new_top
        page.update()

    city_search = TextField(
        hint_text="Enter city name",
        width=200,
        height=40,
        text_size=14,
        border_radius=6,
        on_submit=update_weather,
    )

    search_button = IconButton(
        icon=icons.SEARCH,
        icon_color="white",
        icon_size=20,
        on_click=update_weather,
        bgcolor="lightblue600",
        style=ButtonStyle(
            shape={
                "": RoundedRectangleBorder(radius=8),
            },
        ),
    )

    search_row = Row(
        controls=[
            city_search,
            search_button,
        ],
        alignment="center",
        spacing=10,
    )

    def _expand(e):
        if e.data == "true":
            c.content.controls[1].content.controls[0].height = 560
            c.content.controls[1].content.controls[0].update()
        else:
            c.content.controls[1].content.controls[0].height = 660 * 0.40
            c.content.controls[1].content.controls[0].update()

    def current_temp():
        if current[0] is not None:
            try:
                data = current[0].json()
                temperature = data["main"]["temp"]
                return int(round(temperature))
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error getting temperature: {e}")
                return "N/A"
        return "N/A"

    # New function to create weekly forecast container
    def weekly_forecast_container():
        weekly_data = get_weekly_forecast()
        
        if not weekly_data:
            return Container(
                width=310,
                height=200,
                bgcolor="white10",
                border_radius=20,
                padding=15,
                content=Column(
                    alignment="center",
                    horizontal_alignment="center",
                    controls=[
                        Text("Forecast data not available", color="white")
                    ]
                )
            )
        
        forecast_items = []
        for day in weekly_data:
            day_container = Container(
                width=300,
                height=50,
                border_radius=10,
                bgcolor="white10",
                padding=10,
                margin=margin.only(bottom=5),
                on_click=lambda e, day=day: update_day_weather(day),
                content=Row(
                    alignment="spaceBetween",
                    controls=[
                        Text(day['day'], color="white", size=14),
                        Row(
                            controls=[
                                Text(f"{day['temp']}°C", color="white", size=14),
                                Text(day['description'], color="white70", size=12)
                            ],
                            spacing=10
                        )
                    ]
                )
            )
            forecast_items.append(day_container)
        
        return Container(
            width=310,
            height=250,
            bgcolor="black",
            padding=15,
            margin=margin.only(top=10),
            content=Column(
                controls=[
                    Text("Weekly Forecast", color="white", size=16, weight="bold"),
                    *forecast_items
                ],
                spacing=5,
                scroll="auto"
            )
        )

    def top():
        today_temp = current_temp()
        weather_details = get_weather_details()
        city_name = current[0].json()["name"] if current[0] else "Enter City"

        details_row = Row(
            alignment="center",
            spacing=20,
            controls=[
                Column(
                    horizontal_alignment="center",
                    controls=[
                        Text("Humidity", size=12, weight="w400", color="white70"),
                        Text(
                            f"{weather_details['humidity']}%"
                            if weather_details else "N/A",
                            size=14,
                            weight="bold"
                        ),
                    ]
                ),
                Column(
                    horizontal_alignment="center",
                    controls=[
                        Text("Wind", size=12, weight="w400", color="white70"),
                        Text(
                            f"{weather_details['wind_speed']} m/s"
                            if weather_details else "N/A",
                            size=14,
                            weight="bold"
                        ),
                    ]
                ),
                Column(
                    horizontal_alignment="center",
                    controls=[
                        Text("Pressure", size=12, weight="w400", color="white70"),
                        Text(
                            f"{weather_details['pressure']} hPa"
                            if weather_details else "N/A",
                            size=14,
                            weight="bold"
                        ),
                    ]
                ),
            ]
        )

        top = Container(
            width=310,
            height=660 * 0.40,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["lightblue600", "lightblue900"],
            ),
            border_radius=35,
            animate=animation.Animation(duration=350, curve="decelerate"),
            on_hover=_expand,
            padding=15,
            content=Column(
                alignment="start",
                spacing=10,
                controls=[
                    Row(
                        alignment="center",
                        controls=[
                            Text(
                                city_name,
                                size=16,
                                weight="w500",
                            )
                        ],
                    ),
                    Container(padding=padding.only(bottom=5)),
                    Row(
                        alignment="center",
                        spacing=30,
                        controls=[
                            Column(
                                controls=[
                                    Container(
                                        width=90,
                                        height=90,
                                    )
                                ]
                            ),
                            Column(
                                spacing=5,
                                horizontal_alignment="center",
                                controls=[
                                    Text(
                                        "Today",
                                        size=12,
                                        text_align="center",
                                    ),
                                    Row(
                                        vertical_alignment="start",
                                        spacing=0,
                                        controls=[
                                            Container(
                                                content=Text(
                                                    f"{today_temp}°C"
                                                    if today_temp != "N/A"
                                                    else "N/A",
                                                    size=52,
                                                ),
                                            )
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(padding=padding.only(bottom=10)),
                    Text(
                        weather_details["description"] if weather_details else "N/A",
                        size=14,
                        color="white70",
                        text_align="center",
                    ),
                    Container(padding=padding.only(top=5)),
                    details_row,
                ],
            ),
        )
        return top

    # Main container
    c = Container(
        width=310,
        height=660,
        border_radius=35,
        bgcolor="black",
        padding=10,
        content=Column(
            controls=[
                search_row,
                Container(
                    width=310,
                    height=500,  # Adjusted height for better fit
                    content=Column(
                        controls=[
                            top(),
                            weekly_forecast_container(),
                        ],
                        scroll="auto",
                        spacing=10
                    )
                )
            ],
        ),
    )

    page.add(c)


if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")