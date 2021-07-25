from decouple import config
API_KEY = config('ALPACA_KEY')
SECRET_KEY = config('ALPACA_SECRET_KEY')
ENDPOINT_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(ENDPOINT_URL)
ORDERS_URL = "{}/v2/orders".format(ENDPOINT_URL)
BARS_URL = "https://data.alpaca.markets/v1/bars"
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
