from collections import namedtuple

Asset = namedtuple('Asset', ['symbol', 'position', 'close'])

class VirtualAccount(object):
  def __init__(
      self, cash=0, asset=None, **kwargs):
    self._cash = cash
    self._assets = assets or {}
    self._kwargs = kwargs  

  @property
  def cash(self):
    return self._cash

  def get_asset(self, symbol):
    return self._assets[symbol]

  def update_asset_quote(self, symbol, quote):
    self._assets.setdefault(
        symbol, Asset(
            symbol=symbol, position=0, close=quote)).close = quote

  def execute_asset(self, symbol, amount, action):
    assert action in ('BUY', 'SELL')
    assert symbol in self._assets
    if action == 'SELL': amount *= -1
    self._assets[symbol].position += amount
    self._cash -= self._assets[symbol].close * amount

  def get_assets_value(self):
    assets_mkt_val = sum(
        asset.position * asset.close for asset in self._assets.values())
    return asset_mkt_val

  def get_net_value(self):
    return self._cash + self.get_assets_value()

  def list_assets(self):
    return [asset for asset in self._assets.values() if asset.position]

