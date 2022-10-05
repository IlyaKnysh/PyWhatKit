import os
import time
import webbrowser as web
from platform import system
from typing import Optional

import requests
import wikipedia

from pywhatkit.core import exceptions

if system().lower() in ("windows", "darwin"):
    from PIL import ImageGrab

    def take_screenshot(
        file_name: str = "pywhatkit_screenshot", delay: int = 2, show: bool = True
    ) -> None:
        """Take Screenshot of the Screen"""

        time.sleep(delay)
        screen = ImageGrab.grab()
        if show:
            screen.show(title=file_name)
        screen.save(f"{file_name}.png")

def show_history() -> None:
    """Prints the Log File Generated by the Library"""

    try:
        with open("PyWhatKit_DB.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        print("Log File does not Exist!")
    else:
        if len(content) == 0:
            print("No Logs in File!")
        else:
            print(content)


def info(topic: str, lines: int = 3, return_value: bool = False) -> Optional[str]:
    """Gives Information on the Topic"""

    data = wikipedia.summary(topic, sentences=lines)
    print(data)
    if return_value:
        return data


def playonyt(topic: str, use_api: bool = False, open_video: bool = True) -> str:
    """Play a YouTube Video"""

    if use_api:
        response = requests.get(
            f"https://pywhatkit.herokuapp.com/playonyt?topic={topic}"
        )
        status_code = response.status_code
        if status_code == 200:
            if open_video:
                web.open(response.content.decode("ascii"))
            return response.content.decode("ascii")
        elif 400 <= status_code <= 599:
            raise exceptions.UnableToAccessApi(
                "Unable to access pywhatkit api right now"
            )
    else:
        url = f"https://www.youtube.com/results?q={topic}"
        count = 0
        cont = requests.get(url)
        data = cont.content
        data = str(data)
        lst = data.split('"')
        for i in lst:
            count += 1
            if i == "WEB_PAGE_TYPE_WATCH":
                break
        if lst[count - 5] == "/results":
            raise Exception("No Video Found for this Topic!")

        if open_video:
            web.open(f"https://www.youtube.com{lst[count - 5]}")
        return f"https://www.youtube.com{lst[count - 5]}"


def search(topic: str) -> None:
    """Searches About the Topic on Google"""

    link = f"https://www.google.com/search?q={topic}"
    web.open(link)
