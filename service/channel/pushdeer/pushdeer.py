import json
from typing import Optional, Union
from service.config import Config
import requests
from service.parameters import ParameterResolver
from service.weibo.topn import formatted_top_list


class PushDeer:
    """
    PushDeer Class is used to interact with the PushDeer API to send text, Markdown and image push messages.

    Paramters:
    - server (str): API Server address
    - pushkey (str): PushDeer pushkey (optional)
    """

    endpoint = "/message/push"

    def __init__(self, server: Optional[str] = None, pushkey: Optional[str] = None):
        """
        Initialize the PushDeer class.

        Parameters:
        - server (str): API Server address
        - pushkey (str): PushDeer pushkey (optional)
        """
        self.server = server or Config.PUSHDEER_SERVER_URL
        self.pushkey = pushkey

    def _push(
        self,
        text: str,
        desp: Optional[str] = None,
        server: Optional[str] = None,
        pushkey: Optional[str] = None,
        text_type: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        Internal method: send push request.

        Parameters:
        - text (str): main content of the message
        - desp (str): additional description of the message (optional)
        - server (str): API base address (optional)
        - pushkey (str): pushkey (optional)
        - text_type (str): message type (text, markdown, image)
        - kwargs: other request parameters

        Returns:
        - bool: True if successful, otherwise False
        """
        # Check if pushkey is specified
        pushkey = pushkey or self.pushkey
        if not pushkey:
            raise ValueError("Pushkey must be specified")

        # Send the push request and check the result
        response = self._send_push_request(
            desp, pushkey, server or self.server, text, text_type, **kwargs
        )
        if "content" in response and response["content"].get("result"):
            result = json.loads(response["content"]["result"][0])
            return result.get("success") == "ok"
        return False

    def _send_push_request(
        self,
        desp: Optional[str],
        key: str,
        server: str,
        text: str,
        text_type: Optional[str],
        **kwargs
    ) -> dict:
        """
        Internal method: send HTTP GET request to PushDeer API.

        Parameters:
        - desp (str): additional description of the message (optional)
        - key (str): pushkey
        - server (str): API Server address
        - text (str): main content of the message
        - text_type (str): message type (text, markdown, image)
        - kwargs: other request parameters

        Returns:
        - dict: API response
        """
        params = {
            "pushkey": key,
            "text": text,
            "type": text_type,
            "desp": desp,
        }
        response = requests.get(
            server + self.endpoint, params=params, **kwargs, timeout=10
        )
        response.raise_for_status()
        return response.json()

    def send_text(
        self,
        text: str,
        desp: Optional[str] = None,
        server: Optional[str] = None,
        pushkey: Union[str, list, None] = None,
        **kwargs
    ) -> bool:
        """
        Send a text push message.

        Parameters:
        - text (str): main content of the message
        - desp (str): additional description of the message (optional)
        - server (str): API Server address (optional)
        - pushkey (Union[str, list, None]): pushkey (optional)
        - kwargs: other request parameters

        Returns:
        - bool: True if successful, otherwise False
        """
        return self._push(
            text=text,
            desp=desp,
            server=server,
            pushkey=pushkey,
            text_type="text",
            **kwargs
        )

    def send_markdown(
        self,
        text: str,
        desp: Optional[str] = None,
        server: Optional[str] = None,
        pushkey: Union[str, list, None] = None,
        **kwargs
    ) -> bool:
        """
        Send a Markdown push message.

        Parameters:
        - text (str): main content of the message
        - desp (str): additional description of the message (optional)
        - server (str): API Server address (optional)
        - pushkey (Union[str, list, None]): pushkey (optional)
        - kwargs: other request parameters

        Returns:
        - bool: True if successful, otherwise False
        """
        return self._push(
            text=text,
            desp=desp,
            server=server,
            pushkey=pushkey,
            text_type="markdown",
            **kwargs
        )

    def send_image(
        self,
        image_src: str,
        desp: Optional[str] = None,
        server: Optional[str] = None,
        pushkey: Union[str, list, None] = None,
        **kwargs
    ) -> bool:
        """
        Send an image push message.

        Parameters:
        - image_src (str): URL or Base64 encoding of the image
        - desp (str): additional description of the image (optional)
        - server (str): API Server address (optional)
        - pushkey (Union[str, list, None]): pushkey (optional)
        - kwargs: other request parameters

        Returns:
        - bool: True if successful, otherwise False
        """
        return self._push(
            text=image_src,
            desp=desp,
            server=server,
            pushkey=pushkey,
            text_type="image",
            **kwargs
        )


class PushDeerPlatform:
    """
    PushDeerPlatform Class is used to interact with the PushDeer API to send push messages to multiple devices.

    Paramters:
    - server (str): API Server address
    - pushkey (str): PushDeer pushkey (optional)
    """

    def __init__(self):
        """
        Initialize the PushDeerPlatform class.

        Parameters:
        - server (str): API Server address
        - pushkey (str): PushDeer pushkey (optional)
        """

        self.template_id = Config.TEMPLATE_ID
        self.city = Config.CITY
        self.province = Config.PROVINCE
        self.user_ids = Config.USER_IDS
        self.names = Config.NAMES
        self.love_date = Config.LOVE_DATE
        self.birthday = Config.BIRTHDAY
        self.pushkeys = Config.PUSHDEER_PUSHKEYS

    def push_template_message(self, pushkey: str, name: str) -> None:
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
        api = PushDeer(pushkey=pushkey)
        api.send_markdown("# 早上好，亲爱的\n" + md_str)
        # api.send_markdown("# 早上好，亲爱的", desp=md_str)

    def run(self):
        """
        Trigger function, fetch AccessToken, call weather API, send message to all users.
        """

        for pushkey, name in zip(self.pushkeys, self.names):
            self.push_template_message(pushkey, name)


def pushdeer_example():
    """
    Example usage: send text, markdown and image push messages.
    """
    pushdeer = PushDeer(pushkey="PDU31883TMsywuZ119ZLKvJ3O1zQsyyZFAim8hnEd")

    # Send text message
    pushdeer.send_text("hello this is a test message", desp="optional description")

    # Send Markdown message
    pushdeer.send_markdown(
        "# Crush on you", desp="**optional** description in markdown"
    )

    # Send image message (image URL)
    pushdeer.send_image(
        "https://github.com/easychen/pushdeer/raw/main/doc/image/clipcode.png"
    )


if __name__ == "__main__":
    pushdeer_example()
