import requests


class PriceDollar:
    @classmethod
    def get(cls):
        try:
            url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
            response = requests.get(url)
            response = response.json()
            return response
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    @classmethod
    def get_price(cls):
        price = cls.get()
        price = price[1]['casa']['venta']
        return float(price.replace(',', '.'))
