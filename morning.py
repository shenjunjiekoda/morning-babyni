import argparse
from channel.pushdeer.pushdeer import PushDeerPlatform
from channel.wechat_public_tester.wechat_public_tester import WechatTesterPlatform


def morning(channel: str):
    """
    Send push notifications to the selected channel or all channels.

    Parameters:
    - channel (str): "pushdeer", "wechat" or "all"
    """
    if channel == "pushdeer":
        print("Running PushDeer...")
        
        pushdeer = PushDeerPlatform()
        pushdeer.run()
        
    elif channel == "wechat":
        print("Running WeChat...")
        
        wechat = WechatTesterPlatform()
        wechat.run()
        
    elif channel == "all":
        print("Running ALl...")
        
        pushdeer = PushDeerPlatform()
        pushdeer.run()
        
        wechat = WechatTesterPlatform()
        wechat.run()
        
    else:
        print("Invalid channel. Choose 'pushdeer', 'wechat', or 'all'.")


def main():
    """
    Main function to run the program.
    """
    parser = argparse.ArgumentParser(
        description="Select the channel for morning notifications."
    )

    parser.add_argument(
        "--channel",
        choices=["pushdeer", "wechat", "all"],
        default="pushdeer",
        help="Select which channel to send notification: 'pushdeer', 'wechat', or 'all'.",
    )

    args = parser.parse_args()
    morning(args.channel)


if __name__ == "__main__":
    main()
