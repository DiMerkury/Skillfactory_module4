import requests
import json

from conf import keys

class APIException(Exception):
    pass

class CurrencyConversion:
    
    @staticmethod
    def get_price(quote: str, base: str, amount: str) -> str:

        if quote == base:
            raise APIException(f'Введенные валюты одинаковые: {quote}')

        try:
            currency_quote = keys[quote]
        except KeyError:
            raise APIException(f'Введена неправильная или несуществующая валюта: {quote}')

        try:
            currency_base = keys[base]
        except KeyError:
            raise APIException(f'Введена неправильная или несуществующая валюта: {base}')
        
        try:
            currency_amount = float(amount)
        except ValueError:
            raise APIException(f'Неправильно введено число: {amount}')

        r = requests.get(f'https://www.floatrates.com/daily/{currency_base}.json')
        total_base = float(json.loads(r.content)[currency_quote]['inverseRate']) * currency_amount

        return f'{total_base:.2f}'
    