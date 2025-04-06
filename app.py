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

# API request with error handling
current = fetch_weather_data("London")

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


def main(page: Page):
    # Page setup
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.title = "Weather App"

    def update_weather(e):
        global current
        if not city_search.value:
            page.show_snack_bar(SnackBar(content=Text("Please enter a city name")))
            return
            
        current = fetch_weather_data(city_search.value)
        if current:
            # Create new top container with updated data
            new_top = top()
            # Update the Stack's controls
            c.content.controls[1].controls[0] = new_top
            c.content.controls[1].controls[0].update()
            city_search.value = ""  # Clear the search field
            city_search.update()
            page.update()  # Update the entire page
        else:
            page.show_snack_bar(SnackBar(content=Text("City not found or network error")))

    city_search = TextField(
        hint_text="Enter city name",
        width=200,
        height=40,
        text_size=14,
        border_radius=6,
        on_submit=lambda e: update_weather(e),  # Add this line to handle Enter key
    )

    search_button = IconButton(
        icon=icons.SEARCH,
        icon_color="white",
        icon_size=20,
        on_click=update_weather,  # Make sure this line is present
        bgcolor="lightblue600",   # Optional: add background color
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
        spacing=10,  # Add spacing between search box and button
    )

    def _expand(e):
        if e.data == "true":
            c.content.controls[1].controls[0].height = 560
            c.content.controls[1].controls[0].update()
        else:
            c.content.controls[1].controls[0].height = 660 * 0.40
            c.content.controls[1].controls[0].update()

    def current_temp():
        if current is not None:
            try:
                data = current.json()
                temperature = data["main"]["temp"]
                return int(round(temperature))  # Round to nearest integer
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error getting temperature: {e}")
                return "N/A"
        return "N/A"

    def top():
        today_temp = current_temp()
        weather_details = get_weather_details()

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

        city_name = current.json()["name"] if current else "Enter City"

        top = Container(
            width=310,
            height=660 * 0.40,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["lightblue600", "lightblue900"],  # Fixed color names
            ),
            border_radius=35,
            animate=animation.Animation(duration=350, curve="decelerate"),
            on_hover=lambda e: _expand(e),
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
                                        # Add an image source here if needed
                                        # image_src="./assets/cloudy.png"
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
                Stack(
                    width=310,
                    height=600,  # Adjusted height to accommodate search
                    controls=[
                        top(),
                    ],
                ),
            ],
        ),
    )

    page.add(c)


if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")