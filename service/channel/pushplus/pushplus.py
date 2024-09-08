import json
from typing import Optional
from service.config import Config
import requests
from service.parameters import ParameterResolver
from service.weibo.topn import formatted_top_list


class PushPlus:
    """
    PushPlus Class is used to interact with the PushPlus API to send text, Markdown and image push messages.

    Paramters:
    - server (str): API Server address
    - token (str): PushPlus token (optional)
    """

    endpoint = "/send"

    def __init__(self, server: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize the PushPlus class.

        Parameters:
        - server (str): API Server address
        - token (str): PushPlus token (optional)
        """
        self.server = server or Config.PUSHPLUS_SERVER_URL
        self.token = token

    def _push(
        self,
        token: str,
        server: str,
        title: str,
        content: str,
        template: str,
    ) -> bool:
        """
        Internal method: send push request.

        Parameters:
        - token (str): token
        - server (str): API Server address
        - title (str): message title
        - content (str): message content
        - template (str): message template: html, txt, markdown, json

        Returns:
        - bool: True if successful, otherwise False
        """
        # Check if token is specified
        token = token or self.token
        if not token:
            raise ValueError("token must be specified")

        # Send the push request and check the result
        response = self._send_push_request(
            token, server or self.server, title, content, template
        )
        if "content" in response and response["content"].get("result"):
            result = json.loads(response["content"]["result"][0])
            return result.get("success") == "ok"
        return False

    def _send_push_request(
        self,
        token: str,
        server: str,
        title: str,
        content: str,
        template: str,
    ) -> dict:
        """
        Internal method: send HTTP Post request to PushPlus API, Use Content-Type: application/json.

        Parameters:
        - token (str): token
        - server (str): API Server address
        - title (str): message title
        - content (str): message content
        - template (str): message template: html, txt, markdown, json

        Returns:
        - dict: API response
        """
        params = {
            "token": token,
            "title": title,
            "content": content,
            "template": template,
        }
        # response = requests.get(
        # server + self.endpoint, params=params, timeout=10
        # )
        response = requests.post(
            server + self.endpoint,
            data=json.dumps(params),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def send_markdown(
        self,
        title: str,
        content: str,
        token: Optional[str] = None,
        server: Optional[str] = None,
    ) -> bool:
        """
        Send a Markdown push message.

        Parameters:
        - text (str): main content of the message
        - desp (str): additional description of the message (optional)
        - server (str): API Server address (optional)
        - token (Union[str, list, None]): token (optional)
        - kwargs: other request parameters

        Returns:
        - bool: True if successful, otherwise False
        """
        return self._push(token, server, title, content, "markdown")


class PushPlusPlatform:
    """
    PushPlusPlatform Class is used to interact with the PushPlus API to send push messages to multiple devices.

    Paramters:
    - server (str): API Server address
    - token (str): PushPlus token (optional)
    """

    def __init__(self):
        """
        Initialize the PushPlusPlatform class.

        Parameters:
        - server (str): API Server address
        - token (str): PushPlus token (optional)
        """

        self.template_id = Config.TEMPLATE_ID
        self.city = Config.CITY
        self.province = Config.PROVINCE
        self.user_ids = Config.USER_IDS
        self.names = Config.NAMES
        self.love_date = Config.LOVE_DATE
        self.birthday = Config.BIRTHDAY
        self.tokens = Config.PUSHPLUS_TOKENS

    def push_template_message(self, token: str, name: str) -> None:
        """
        Send a template message to a single user.
        """
        weather_data = ParameterResolver.get_weather_data()
        date_str = ParameterResolver.get_today_and_weekday()
        love_day, birthday_day = ParameterResolver.calculate_days()
        daily_quote = ParameterResolver.get_daily_quote()
        weibo_top20 = formatted_top_list(20, True)
        dict_data = {
            "date": date_str,
            "name": name,
            "city": self.city,
            "weather": weather_data[0],
            "max_temperature": weather_data[1],
            "min_temperature": weather_data[2],
            "love_day": love_day,
            "birthday": birthday_day,
            "one": daily_quote,
            "weibo_topn": weibo_top20,
        }

        md_str = ParameterResolver.render_template("template.md", dict_data)
        api = PushPlus(token=token)
        api.send_markdown("来自亲爱的消息", "# 早上好，亲爱的\n" + md_str)

    def run(self):
        """
        Trigger function, fetch AccessToken, call weather API, send message to all users.
        """

        for token, name in zip(self.tokens, self.names):
            self.push_template_message(token, name)


if __name__ == "__main__":
    wrapper = PushPlusPlatform()
    wrapper.run()
