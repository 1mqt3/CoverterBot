import requests

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f"http://data.fixer.io/api/latest?access_key=955c05ad07582a8ba52fec5e6eb9b40a&symbols={base},{quote}"
        response = requests.get(url)
        data = response.json()

        if data["success"]:
            base_rate = data["rates"][base]
            quote_rate = data["rates"][quote]
            price = (quote_rate / base_rate) * amount
            return round(price, 2)
        else:
            raise APIException(
                f"Не удалось получить курс валют. Код ошибки: {data['error']['code']}. Сообщение об ошибке: {data['error']['info']}")