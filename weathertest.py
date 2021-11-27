

from bs4 import BeautifulSoup as bs
import requests
import contextlib
import argparse

#function for getting weather data from Google weather

def get_data():
    request = requests.Session()
    #search for your own user agent on Google
    request.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    dataone = request.get(website)

    soup = bs(dataone.text, "html.parser")

    result = {}
    # extract current weather data of a city, including temperature weather condition, precipitation, humidity and wind
    result['city'] = soup.find("div", attrs={"id": "wob_loc"}).text
    result['temp'] = soup.find("span", attrs={"id": "wob_tm"}).text
    result['daytime'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weatherdesc'] = soup.find("span", attrs={"id": "wob_dc"}).text
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text

    #extract data on today as well as next seven days' weather condition and temperature range
    followingdays = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for nextday in days.findAll("div", attrs={"class": "wob_df"}):
        dayday = nextday.findAll("div")[0].attrs['aria-label']
        nextdayweatherdesc = nextday.find("img").attrs["alt"]
        nextdaytemp = nextday.findAll("span", {"class": "wob_t"})
        max_temp = nextdaytemp[0].text
        min_temp = nextdaytemp[2].text
        followingdays.append({"name": dayday, "weather": nextdayweatherdesc, "max_temp": max_temp, "min_temp": min_temp})
    # append to result
    result['followingdays'] = followingdays
    return result

#parse arguments
#Insert the city here
if __name__ == "__main__":
    website = "https://www.google.co.uk/search?q=weather"
    parser = argparse.ArgumentParser()
    parser.add_argument("city", nargs="?", default="Los Angeles")
    args = parser.parse_args()
    city = args.city
    if city:
        city = city.replace(" ", "+")
        website += f"+{city}"

    # gather all data
    data = get_data()

    #other var for nextdays' weather
    unit = "°C"
    hyphen = "-"

    # extract all weather data to a text file
file_path = 'weatherfile.txt'
with open(file_path, "w") as o:
    with contextlib.redirect_stdout(o):
        print("Location:", data["city"])
        print("Current day and time:", data["daytime"])
        print(f"Current Temperature: {data['temp']}", unit)
        print("Current weather:", data['weatherdesc'])
        print("Precipitation:", data["precipitation"])
        print("Humidity:", data["humidity"])
        print("Wind:", data["wind"])
        print("Today and next 7 days' weather:")
        for nextdayweather in data["followingdays"]:
            print("{"*1, nextdayweather["name"], "}"*1)
            print("Status:", nextdayweather["weather"])
            print("Temperature Range: " + nextdayweather['min_temp'], hyphen, nextdayweather['max_temp'], unit)

#open file
f = open 'filepath', "r")
