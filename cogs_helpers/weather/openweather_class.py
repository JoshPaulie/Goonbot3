import aiohttp

from config import BotConfig


def pretty_temp(temp: float):
    temp = round(temp)
    temp = str(temp) + "°F"
    return temp


class City:
    def __init__(self, city_json):
        self.city_json = city_json
        self.temps = self.city_json.get("main")

        self.name = self.city_json.get("name")
        self.temp_current = pretty_temp(self.temps.get("temp"))
        self.temp_min = pretty_temp(self.temps.get("temp_min"))
        self.temp_max = pretty_temp(self.temps.get("temp_max"))
        self.feels_like = pretty_temp(self.temps.get("feels_like"))


class OpenWeather:
    def __init__(self, units="imperial"):
        self.units = units
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.api_key = BotConfig.Keys.openweather
        self.url = f"{self.base_url}?appid={self.api_key}&units={self.units}"

    async def current_city_by_zip(self, zip_code: int):
        url = self.url + f"&zip={str(zip_code)},us"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                json = await response.json()
                return City(json)
