import json
import requests

from Properties import currency


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(price_from, price_to, quantity):
        if price_from == price_to:
            raise ConvertionException("Невозможно перевести одинаковые валюты!")

        try:
            price_from_ticker = currency[price_from]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {price_from}")

        try:
            price_to_ticker = currency[price_to]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {price_to}")

        try:
            quantity = float(quantity)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {quantity}")
        else:
            if quantity <= 0:
                raise ConvertionException(f"Не удалось обработать количество {quantity}")

        r = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={price_from_ticker}&tsyms={price_to_ticker}")

        total = json.loads(r.content)[currency[price_to]]

        return total
