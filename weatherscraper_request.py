from requests_html import HTMLSession
import requests

#scrape current weather data from Google with requests_html
request = HTMLSession()
#insert city here
city = ""
website = f'https://www.google.com/search?q=weather+{city}'
#Getting data from Google. Search for your user agent and insert it in headers
data = request.get(website, headers={''})
#variables for current weather
daytime = data.html.find('div.wob_dts', first=True).text
temperature = data.html.find('span#wob_tm', first=True).text
unit = '°C'
description = (data.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text)
precipitation = data.html.find('span#wob_pp', first=True).text
humidity = data.html.find('span#wob_hm', first=True).text
wind = data.html.find('span#wob_ws.wob_t', first=True).text
print("\nCity: " + city)
print("\nDay and Time : " + daytime)
print("\nCurrent Temperature: " + temperature,unit)
print("\nPrecipitation: " + precipitation)
print ("\nHumidity: " + humidity)
print("\nWind: " + wind)
print("\nWeather Condition: " + description)
