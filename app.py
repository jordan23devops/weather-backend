from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Dictionary of supported cities as required by the assignment
CITIES = {
    "new_york": "New York",
    "sydney": "Sydney",
    "cape_town": "Cape Town",
    "bangkok": "Bangkok"
}

# Fetch the API Key from an environment variable (DevOps Best Practice)
API_KEY = os.environ.get('WEATHER_API_KEY')

@app.route('/weather/<city_key>', methods=['GET'])
def get_weather(city_key):
    city_name = CITIES.get(city_key.lower())
    
    if not city_name:
        return jsonify({"error": "City not supported. Use: new_york, sydney, cape_town, bangkok"}), 404

    if not API_KEY:
        return jsonify({"error": "API Key is missing"}), 500

    # Build the URL according to the project guidelines
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Return JSON with the required fields: temperature, description, humidity, and wind speed
        return jsonify({
            "city": city_name,
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # The application listens on port 5000 as required
    app.run(host='0.0.0.0', port=5000)
