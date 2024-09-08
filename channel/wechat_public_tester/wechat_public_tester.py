from datetime import date
import requests
from channel.config import Config
from channel.parameters import ParameterResolver


class WechatTesterPlatform:
    """
    WechatTesterPlatform Class is used to interact with WeChat public test account, send template message.
    """

    def __init__(self):
        """
        Init WechatTesterPlatform class, load config.
        """
        self.server_url = Config.WECHAT_TOKEN_URL
        self.app_id = Config.APP_ID
        self.app_secret = Config.APP_SECRET
        self.template_id = Config.TEMPLATE_ID
        self.province = Config.PROVINCE
        self.city = Config.CITY
        self.user_ids = Config.USER_IDS
        self.names = Config.NAMES
        self.love_date = Config.LOVE_DATE
        self.birthday = Config.BIRTHDAY

    def fetch_access_token(self) -> str:
        """
        Fetch access_token from WeChat public platform.

        Returns:
        - str: resp_access_token string
        """
        url = f"{self.server_url}?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        try:
            response = requests.get(url, timeout=10).json()
            access_token = response.get("access_token")
            if access_token:
                return access_token
            raise ValueError("No access_token found in response")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except ValueError as e:
            print(f"Response error: {e}")
            return None

    def send_message(self, user_id: str, name: str, access_token: str) -> None:
        """
        Send a template message to a wechat user.

        Parameters:
        - user_id (str): user wechat id
        - name (str): user name
        - access_token (str): wechat api access_token
        """
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"

        weather, max_temp, min_temp = ParameterResolver.get_weather_data()
        date_str = ParameterResolver.get_today_and_weekday()
        love_days, birthday_days = ParameterResolver.calculate_days()

        data = {
            "touser": user_id,
            "template_id": self.template_id,
            "url": "http://weixin.qq.com/download",
            "topcolor": "#FF0000",
            "data": {
                "date": {"value": date_str, "color": "#00FFFF"},
                "name": {"value": name, "color": "#00FF00"},
                "city": {"value": self.city, "color": "#808A87"},
                "weather": {"value": weather, "color": "#ED9121"},
                "max_temperature": {"value": max_temp, "color": "#FF6100"},
                "min_temperature": {"value": min_temp, "color": "#00FF00"},
                "love_day": {"value": love_days, "color": "#87CEEB"},
                "birthday": {"value": birthday_days, "color": "#FF8000"},
                "one": {
                    "value": ParameterResolver.get_daily_quote(),
                    "color": "#808A87",
                },
            },
        }

        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            print(f"Message sent successfully to {user_id}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def run(self):
        """
        Trigger function, fetch AccessToken, call weather API, send message to all users.
        """
        access_token = self.fetch_access_token()
        if not access_token:
            print("Failed to fetch access token.")
            return

        for user_id, name in zip(self.user_ids, self.names):
            self.send_message(user_id, name, access_token)
