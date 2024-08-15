import json
import os
import random
import time
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


class GloboProgramming:


    def __init__(self, api_keys: list) -> None:
        self.api_keys = api_keys
        self.sa_url = "https://api.scrapingant.com/v2/general"
        self.__cache = {}
        self.channels = self.load_channels()
        self.default_ttl = os.getenv('DEFAULT_TTL') or 60


    def __set_cache(self, key, value, ttl=30):
        self.__cache[key] = {
            "ttl": time.time() + ttl,
            "value": value
        }


    def __unset_cache(self, key):
        return self.__cache.pop(key)


    def __get_cache(self, key):
        cache = self.__cache.get(key, False)
        if not cache:
            return False

        now = time.time()
        ttl = cache.get("ttl", now)

        if now > ttl:
            self.__unset_cache(key)
            return False

        return self.__cache[key].get("value", None)


    def __make_request(self, channel_url):
        params = {
            "url": channel_url,
            "x-api-key": random.choice(self.api_keys)
            }
        url = f"{self.sa_url}?{urlencode(params)}"

        result = requests.get(url)
        if result.status_code != 200:
            print(result.json().get("detail", "Error when making request."))
            return False

        return result


    def __get_soup(self, channel_url):
        result = self.__get_cache(channel_url)
        if not result:
            result = self.__make_request(channel_url)
            self.__set_cache(channel_url, result, self.default_ttl)

        if not result:
            return False

        html = result.text
        soup = BeautifulSoup(html, "html.parser")
        return soup


    def __get_failed_response(self, message):
        return {
            "status": False,
            "message": message,
            "result": None
        }


    def get_channel_programs(self, channel_url):
        channel_programs = []

        soup = self.__get_soup(channel_url)
        if not soup:
            return False

        # Find all divs with the "accordion" class that contain program information
        programs = soup.find_all("div", {"class": "accordion"})

        for program in programs:
            # Try to find the ID of the program
            try:
                program_id = program.attrs["id"]
                program_id = int(program_id) if program_id else None
            except (AttributeError, ValueError, IndexError):
                program_id = None

            # Try to find the name of the program
            program_name = program.find("div", {"class": "accordionTitle__name"})
            program_name = program_name.text.strip() if program_name else None

            # Check if the program is live
            program_live = "accordion--live" in program.attrs.get("class", [])

            # Try to find the program time
            program_time = program.find("div", {"class": "accordionTitle__time"})
            program_time = program_time.text.strip() if program_time else None

            # Adjust the time if the program is live
            if program_live and "TV" in program_time:
                program_time = program_time.split("TV")[1].strip()

            # If there is a previous program, set the endTime to the current time
            if channel_programs:
                channel_programs[-1]["endTime"] = program_time

            # Try to find the program logo
            logo_div = program.find("div", {"class": "accordionTitle__logo"})
            logo = logo_div.img.attrs["src"] if logo_div and logo_div.img else False

            channel_program = {
                "id": program_id,
                "name": program_name,
                "time": program_time,
                "endTime": None,
                "logo": logo,
                "live": program_live,
            }

            # If the program is live, we extract more information
            if program_live:
                # Try to find the preview image
                try:
                    program_preview = program.picture.img.attrs["src"]
                except AttributeError:
                    background_style = program.find("div", {"class": "poster__background"})
                    if background_style and "style" in background_style.attrs:
                        program_preview = background_style.attrs["style"].split('"')[1]
                    else:
                        program_preview = None

                # Try to find the synopsis of the program
                program_synopsis = program.find("p", {"class": "accordion-panel__synopsis"})
                program_synopsis = program_synopsis.text.strip() if program_synopsis else None

                # Try to find the genre of the program
                genre_div = program.find("div", {"class": "genre-badge"})
                genre = genre_div.find_all("span")[-1].text.strip() if genre_div else None

                # Try to find the program's rating
                parental_rating_div = program.find("svg", {"class": "parental-rating"})
                try:
                    parental_rating = int(parental_rating_div.find("title").text.split(": ")[1].split(" ")[0]) if parental_rating_div else None
                except (AttributeError, ValueError, IndexError):
                    parental_rating = None

                # Adds new information to the program dictionary
                channel_program["preview"] = program_preview
                channel_program["synopsis"] = program_synopsis
                channel_program["genre"] = genre
                channel_program["parentalRating"] = parental_rating

            # Add the program to the program list
            channel_programs.append(channel_program)
        return channel_programs


    def load_channels(self):
        try:
            with open("./data/channels.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f"Error loading file: {e}")
            return None


    def find_channel(self, code):
        if not self.channels:
            return False

        for category in self.channels.keys():
            channels_list = self.channels[category]["channels"]
            for channel_code in channels_list:
                if channel_code == code:
                    channel = self.channels[category]["channels"][channel_code]
                    channel["category"] = category
                    return channel

        return None


    def find_channels(self, name):
        if not self.channels:
            return False

        results = []
        for category in self.channels.keys():
            channels_list = self.channels[category]["channels"]
            for channel_code in channels_list:
                if name in channel_code:
                    channel = self.channels[category]["channels"][channel_code]
                    channel["category"] = category
                    results.append(channel)

        return results


    def load_channel_programs(self, channel_code):
        channel = self.find_channel(channel_code)

        if not channel:
            return self.__get_failed_response("The channel name entered does not exist. See the channels available at https://github.com/juniorkrz/globo-programming-api/blob/main/docs/Channels.MD")

        channel_url = channel.get("url")

        if not channel_url:
            return self.__get_failed_response("Unable to get channel URL.")

        programs = self.get_channel_programs(channel_url)

        if not programs:
            return self.__get_failed_response("Unable to retrieve channel schedule.")

        live_now = next((program for program in programs if program["live"]), None)

        result = {
            "name": channel.get("name"),
            "code": channel_code,
            "category": channel.get("category"),
            "liveNow": live_now,
            "programs": programs
        }

        return {
            "status": True,
            "message": "Success",
            "result": result
        }

# For tests
if __name__ == "__main__":
    prog = GloboProgramming(["you_token_here"])
    result = prog.load_channel_programs('globo-brasilia')
    print(result)