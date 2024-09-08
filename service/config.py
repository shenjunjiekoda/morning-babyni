import os


class Config:
    """
    Read environment variables, including WeChat public account configuration, pushdeer configuration, and user information.
    """


    NAMES = os.getenv("NAMES", "").split(",")
    PROVINCE = os.getenv("PROVINCE")
    CITY = os.getenv("CITY")
    BIRTHDAY = os.getenv("BIRTHDAY")
    LOVE_DATE = os.getenv("LOVE_DATE")

    # wechat public tester
    WECHAT_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
    APP_ID = os.getenv("APP_ID")
    APP_SECRET = os.getenv("APP_SECRET")
    TEMPLATE_ID = os.getenv("TEMPLATE_ID")
    USER_IDS = os.getenv("USER_IDS", "").split(",")  # same order as NAMES

    # pushdeer config
    PUSHDEER_SERVER_URL = "https://api2.pushdeer.com"
    PUSHDEER_PUSHKEYS = os.getenv("PUSHDEER_PUSHKEYS").split(",")
    # pushplus config
    PUSHPLUS_SERVER_URL = "https://www.pushplus.plus"
    PUSHPLUS_TOKENS = os.getenv("PUSHPLUS_TOKENS").split(",")
