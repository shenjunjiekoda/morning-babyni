from datetime import date
import requests
from config import Config
from weather_api import WeatherAPI
import cityinfo


def fetch_access_token():
    """
    Fetch access_token from WeChat public platform.

    Returns:
    - str: resp_access_token string
    """
    url = (
        f"{Config.WECHAT_TOKEN_URL}?"
        f"grant_type=client_credential&appid={Config.APP_ID}&secret={Config.APP_SECRET}"
    )

    try:
        response = requests.get(url, timeout=10).json()
        resp_access_token = response.get("access_token")
        if resp_access_token:
            return resp_access_token
        raise ValueError("No access_token found in response")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Response error: {e}")
        return None


def get_daily_quote():
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
            print("Structure of daily quote page has changed, please update the code。")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def calculate_days(love_date, birthday):
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
        love_days = (today - date.fromisoformat(love_date)).days
    except ValueError as exc:
        raise ValueError("Invalid love_date format. Expected 'YYYY-MM-DD'.") from exc

    try:
        birthday_next = date(
            today.year, int(birthday.split("-")[1]), int(birthday.split("-")[2])
        )
    except ValueError as exc:
        raise ValueError("Invalid birthday format. Expected 'YYYY-MM-DD'.") from exc

    if today > birthday_next:
        try:
            birthday_next = date(today.year + 1, birthday_next.month, birthday_next.day)
        except ValueError as exc:
            raise ValueError(
                "Invalid birthday date. The date does not exist in the next year."
            ) from exc

    birthday_days = (birthday_next - today).days

    return love_days, birthday_days


def send_message(user_id, name, access_token, weather_data):
    """
    向指定用户发送微信模板消息。

    参数:
    - user_id (str): 接收消息的用户 ID
    - name (str): 用户昵称
    - access_token (str): 微信 API 的 access_token
    - weather_data (tuple): 包含天气描述、最高温度、最低温度的元组
    """
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"

    today = date.today()
    week = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][
        today.weekday()
    ]

    love_days, birthday_days = calculate_days(Config.LOVE_DATE, Config.BIRTHDAY)

    data = {
        "touser": user_id,
        "template_id": Config.TEMPLATE_ID,
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {"value": f"{today} {week}", "color": "#00FFFF"},
            "name": {"value": name, "color": "#00FF00"},
            "city": {"value": Config.CITY, "color": "#808A87"},
            "weather": {"value": weather_data[0], "color": "#ED9121"},
            "max_temperature": {"value": weather_data[1], "color": "#FF6100"},
            "min_temperature": {"value": weather_data[2], "color": "#00FF00"},
            "love_day": {"value": love_days, "color": "#87CEEB"},
            "birthday": {"value": birthday_days, "color": "#FF8000"},
            "one": {"value": get_daily_quote(), "color": "#808A87"},
        },
    }

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def main():
    """
    Main entry point, get AccessToken, call weather API, send message to users.
    """
    access_token = fetch_access_token()

    weather_data = WeatherAPI.get_weather(
        Config.PROVINCE, Config.CITY, cityinfo.cityInfo
    )

    for user_id, name in zip(Config.USER_IDS, Config.NAMES):
        send_message(user_id, name, access_token, weather_data)


if __name__ == "__main__":
    main()
