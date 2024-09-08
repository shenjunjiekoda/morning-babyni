from datetime import date
import re
import requests
from service.config import Config
import service.weather.cityinfo as cityinfo
from service.weather.weather_api import WeatherAPI


class ParameterResolver:
    """
    Resolves parameters in the morning babyni template.
    """

    @staticmethod
    def calculate_days() -> tuple:
        """
        Calculate the number of days since the date of the first love and the number of days until the next birthday.

        Parameters:
        - love_date (str): love date, format is 'YYYY-MM-DD'
        - birthday (str): birthday date, format is 'YYYY-MM-DD'

        Returns:
        - tuple: (number of days since the date of the first love, number of days until the next birthday)
        """
        today = date.today()

        try:
            love_days = (today - date.fromisoformat(Config.LOVE_DATE)).days
        except ValueError as exc:
            raise ValueError(
                "Invalid love_date format. Expected 'YYYY-MM-DD'."
            ) from exc

        try:
            birthday_next = date(
                today.year,
                int(Config.BIRTHDAY.split("-")[1]),
                int(Config.BIRTHDAY.split("-")[2]),
            )
        except ValueError as exc:
            raise ValueError("Invalid birthday format. Expected 'YYYY-MM-DD'.") from exc

        if today > birthday_next:
            birthday_next = date(today.year + 1, birthday_next.month, birthday_next.day)

        birthday_days = (birthday_next - today).days

        return love_days, birthday_days

    @staticmethod
    def get_daily_quote() -> str:
        """
        Get a random quote from the Daily Qiushi website.

        Returns:
        - str: a random quote
        """
        url = "http://www.wufazhuce.com/"
        try:
            response = requests.get(url, timeout=10)
            response.encoding = "utf-8"
            text = response.text
            if "fp-one-cita-wrapper" in text and "fp-one-cita" in text:
                return (
                    text.split("fp-one-cita-wrapper")[1]
                    .split("fp-one-cita")[1]
                    .split(">")[2]
                    .split("<")[0]
                )
            else:
                print(
                    "Structure of daily quote page has changed, please update the code。"
                )
                return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    @staticmethod
    def get_weather_data():
        """
        Get weather data from weather API.

        Returns:
        - tuple: A tuple containing the weather description, high temperature, and low temperature.
        """
        return WeatherAPI.get_weather(Config.PROVINCE, Config.CITY, cityinfo.cityInfo)

    @staticmethod
    def get_today_and_weekday() -> str:
        """
        Get the current date and weekday.

        Returns:
        - str: the current date and weekday
        """
        today = date.today()
        weekday = [
            "星期日",
            "星期一",
            "星期二",
            "星期三",
            "星期四",
            "星期五",
            "星期六",
        ][today.weekday()]
        return f"{today} {weekday}"

    @staticmethod
    def render_template(template_path, data) -> str:
        """
        Read a template file and replaces placeholders with the values passed in the data dictionary.

        Parameters:
        - template_path (str): path of the template file
        - data (dict): a dictionary containing the variables to be replaced

        Returns:
        - str: the processed template string
        """
        # Read the template file
        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()

        # Regex pattern to match '{{variable_name.DATA}}'
        pattern = re.compile(r"{{(.*?)\.DATA}}")

        # Substitute the placeholders with the values passed in the data dictionary.
        result = pattern.sub(
            lambda match: str(data.get(match.group(1), "")), template_content
        )

        return result
