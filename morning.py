import argparse
from service.channel.pushdeer.pushdeer import PushDeerPlatform
from service.channel.pushplus.pushplus import PushPlusPlatform
from service.channel.wechat_public_tester.wechat_public_tester import (
    WechatTesterPlatform,
)


def morning(channel: str):
    """
    Send push notifications to the selected channel or all channels.

    Parameters:
    - channel (str): "pushdeer", "wechat", "pushplus or "all"
    """
    if channel == "pushdeer":
        print("Running PushDeer...")
        PushDeerPlatform().run()

    elif channel == "wechat":
        print("Running WeChat...")

        WechatTesterPlatform().run()

    elif channel == "pushplus":
        print("Running PushPlus...")

        PushPlusPlatform().run()

    elif channel == "all":
        print("Running ALl...")

        PushDeerPlatform().run()
        WechatTesterPlatform().run()
        PushPlusPlatform().run()

    else:
        print("Invalid channel. Choose 'pushdeer', 'wechat', 'pushplus' or 'all'.")


def main():
    """
    Main function to run the program.
    """
    parser = argparse.ArgumentParser(
        description="Select the channel for morning notifications."
    )

    parser.add_argument(
        "--channel",
        choices=["pushdeer", "wechat", "pushplus", "all"],
        default="pushdeer",
        help="Select which channel to send notification: 'pushdeer', 'wechat', 'pushplus' or 'all'.",
    )

    args = parser.parse_args()
    morning(args.channel)


if __name__ == "__main__":
    main()
