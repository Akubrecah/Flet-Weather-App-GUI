# Flet Weather App ⛅

A beautiful and responsive weather application built with Python and Flet framework that provides real-time weather information with an elegant user interface.

## ✨ Features

- 🌡️ Real-time weather data from OpenWeatherMap API
- 🔍 Intuitive city search functionality
- 📊 Detailed weather information:
  - Temperature in Celsius
  - Weather description
  - Humidity levels
  - Wind speed
  - Atmospheric pressure
- 💫 Smooth animations and transitions
- 🎨 Modern, clean interface
- ⚡ Fast and responsive design
- 🛡️ Robust error handling

## 📸 Screenshots

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenWeatherMap API key
- Git (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flet-weather-app.git
cd flet-weather-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```python
# Create api_key.py file
API_KEY = "your_openweathermap_api_key"
```

4. Run the app:
```bash
python app.py
```

## 🏗️ Project Structure

```
flet-weather-app/
├── app.py              # Main application file
├── api_key.py         # API key configuration
├── assets/            # Images and assets
│   └── screenshot.png
├── requirements.txt   # Project dependencies
├── .gitignore        # Git ignore file
└── README.md         # Project documentation
```

## 💻 Usage

1. Launch the application
2. Enter a city name in the search box
3. Press Enter or click the search icon
4. View detailed weather information for the selected city

## 🔧 Configuration

To use your own OpenWeatherMap API key:
1. Sign up at [OpenWeatherMap](https://openweathermap.org/)
2. Generate an API key
3. Create `api_key.py` in the project root
4. Add your key: `API_KEY = "your_key_here"`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👏 Acknowledgments

- [Flet Framework](https://flet.dev/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Python Requests Library](https://requests.readthedocs.io/)

---

<div align="center">
Made with ❤️ and Python
</div>
