import time
import json
import requests


class WeatherAPI:
    """
    WeatherAPI Class is used to get weather information from weather.com.cn.
    """

    @staticmethod
    def get_weather(province, city, city_info):
        """
        Get specific weather information of a city from weather.com.cn.

        Parameters:
        - province (str): Province name
        - city (str): City name
        - city_info (dict): Dictionary containing the mapping of province and city to AREAID.

        Returns:
        - tuple: A tuple containing the weather description, high temperature, and low temperature.
        """
        city_id = city_info[province][city]["AREAID"]
        t = int(round(time.time() * 1000))  # milliseconds since epoch
        url = f"http://d1.weather.com.cn/dingzhi/{city_id}.html?_={t}"

        headers = {
            "Referer": f"http://www.weather.com.cn/weather1d/{city_id}.shtml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"
        response_data = response.text.split(";")[0].split("=")[-1]
        weather_json = json.loads(response_data)

        weather_info = weather_json["weatherinfo"]
        weather = weather_info["weather"]  # Weather description
        temp = weather_info["temp"]  # High temperature
        tempn = weather_info["tempn"]  # Low temperature

        return weather, temp, tempn
