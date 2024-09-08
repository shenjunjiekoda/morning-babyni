import json
from http.server import BaseHTTPRequestHandler
import requests


def fetch_weibo_hot_search() -> list:
    """
    Fetch Weibo hot search data from the Weibo API.

    Returns:
    - list: A list of dictionaries containing hot search data, including title, url, num, and hot level.
    """
    url = "https://weibo.com/ajax/side/hotSearch"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json().get("data", {}).get("realtime", [])
    return []


def parse_hot_search_data(data_json: list) -> list:
    """
    Parse the raw hot search data from Weibo and format it into a list of dictionaries.

    Parameters:
    - data_json (list): The raw hot search data from Weibo.

    Returns:
    - list: A list of formatted hot search data.
    """
    parsed_data = []
    for item in data_json:
        if "is_ad" in item:
            continue

        rank = get_rank(item)

        search_data = {
            "title": item.get("note", ""),
            "url": f"https://s.weibo.com/weibo?q=%23{item.get('word', '')}%23",
            "num": item.get("num", ""),
            "rank": rank,
        }
        parsed_data.append(search_data)

    parsed_data.sort(key=lambda x: x["rank"])

    return parsed_data


def get_rank(item: dict) -> str:
    """
    Determine the rank based on the item's attributes.

    Parameters:
    - item (dict): A dictionary representing a hot search item.

    Returns:
    - str: The rank label for the hot search item.
    """
    return item.get("rank")


def get_top_list(topn: int = 50) -> list:
    """
    Fetch and parse Weibo hot search data.

    Parameters:
    - topn (int): The number of top search items to return, cannot be greater than 50. Default is 50

    Returns:
    - list: A list of dictionaries containing formatted hot search data.
    """
    raw_data = fetch_weibo_hot_search()
    top50_data = parse_hot_search_data(raw_data[:50])
    return top50_data[:topn]


def formatted_hot_search_list(hot_search_list: list, markdown: bool = False) -> str:
    """
    Convert the list of hot search items into a formatted string.

    Parameters:
    - hot_search_list (list): A list of dictionaries containing hot search data.
    - markdown (bool): Whether to format the output as Markdown. Default is False

    Returns:
    - str: A formatted string where each hot search item is displayed in a single line.
    """
    formatted_list = []

    for item in hot_search_list:
        rank = item.get("rank")
        title = item.get("title", "")
        url = item.get("url", "")
        if markdown:
            formatted_list.append(f"[\[{rank + 1}\] {title}]({url})")
            # formatted_list.append(url) # Pushdeer cannot parse links in markdown
        else:
            formatted_list.append(f"[{rank + 1}] {title} ({url})")

    return "\n\n".join(formatted_list)


def formatted_top_list(topn: int = 50, markdown: bool = False) -> str:
    """
    Fetch and parse Weibo hot search data.

    Parameters:
    - topn (int): The number of top search items to return, cannot be greater than 50. Default is 50
    - markdown (bool): Whether to format the output as Markdown. Default is False

    Returns:
    - str: A formatted string where each hot search item is displayed in a single line.
    """
    return formatted_hot_search_list(get_top_list(topn), markdown)


class WeiboHotSearchHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler class for serving Weibo hot search data in JSON format.
    """

    def do_GET(self, topn: int = 20):
        """
        Handle GET requests by sending the Weibo hot search data as a JSON response.
        """
        data = get_top_list(topn)
        self._send_response(data)

    def _send_response(self, data: list):
        """
        Helper method to send the JSON response.

        Parameters:
        - data (list): The hot search data to be sent in the response.
        """
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


if __name__ == "__main__":
    # print(json.dumps(get_top_list(20), indent=4, ensure_ascii=False))
    print(formatted_top_list(20, True))
