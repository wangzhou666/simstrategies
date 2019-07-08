class VirtualAsset(object):
  def __init__(self, symbol, position, close):
    self._symbol = symbol
    self._position = position
    self._close = close

  @property
  def symbol(self):
    return self._symbol

  @property
  def position(self):
    return self._position

  @property
  def close(self):
    return self._close

  @property
  def mkt_val(self):
    return self._position * self._close

  @position.setter
  def position(self, val):
    self._position = val

  @close.setter
  def close(self, val):
    self._close = val
  

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
        symbol, VirtualAsset(
            symbol=symbol, position=0, close=quote)).close = quote

  def execute_asset(self, symbol, amount, action):
    assert action in ('BUY', 'SELL')
    assert symbol in self._assets
    if action == 'SELL': amount *= -1
    self._assets[symbol].position += amount
    self._cash -= self._assets[symbol].close * amount

  def get_assets_value(self):
    total_mkt_val = sum(asset.mkt_val for asset in self._assets.values())
    return total_mkt_val

  def get_net_value(self):
    return self._cash + self.get_assets_value()

  def list_assets(self):
    return [asset for asset in self._assets.values() if asset.position]

