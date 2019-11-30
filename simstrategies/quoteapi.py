import requests

class AlphaVantageClient(object):

  _baseurl = 'https://www.alphavantage.co/query'

  def __init__(self, apikey=None):
    self._apikey = apikey

  def load_daily_adjusted(
      self, symbol=None, outputsize='full'):
    assert outputsize in ('full', 'compact')
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'outputsize': outputsize,
        'datatype': 'json',
        'apikey': self._apikey,
    }
    res = requests.get(self._baseurl, params=params).json()
    return res['Time Series (Daily)']

