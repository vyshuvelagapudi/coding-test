from flask import Flask
from src.query import *
from src.weather_data import *
import json

app = Flask(__name__)

@app.route('/api/weather/', defaults={'date': None})
@app.route('/api/weather/<date>')
def weather(date):
	weather_data = get_weather_data(date)
	json_output = json.dumps(weather_data)
	return json_output
	
@app.route('/api/weather_data/stats/', defaults={'year': None})
@app.route('/api/weather_data/stats/<year>')
def weather_stats(year):
	weather_data_stats = get_weather_data_stats(year)
	json_output = json.dumps(weather_data_stats)
	return json_output

if __name__ == '__main__':
	task() # Loading Data
	app.run()
