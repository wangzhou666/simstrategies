class Strategy(object):
  def apply(self):
    raise NotImplementedError()


class ScaledETFStrategy():
  def __init__(
      self, account, track_symbol, amplifier=1, **kwargs):
    self._acc = account
    self._sym = symbol
    self._amp = amplifier
    self._kwargs = kwargs

  def apply(self):
    """ Apply scaled ETF strategy to account.

       Adjust the account holdings so that:
        - assets_value / net_value == amplifier
        - the account only hold asset with "self._sym"
       Steps:
        1. clear all other assets than "self._sym"
        2. adjust the position of "self._sym"
       When:
        - |amp| > 1, it leverages
        - |amp| < 1, it deleverages
        - amp > 0, it longs
        - amp < 0, it shorts
    """
    assets = self._acc.list_assets()
    for ast in assets:
      if ast.symbol == self._sym: continue
      self._acc.execute_asset(ast.symbol, ast.position, 'SELL')

    tgt_cash = (1 - self._amp) * self._acc.get_net_value()
    spending_cash = self._acc.cash - tgt_cash
    delta_position = spending_cash / self._acc.get_asset(self._sym).close
    if not self._kwargs.get('allow_float_position'):
      delta_position = int(delta_position)
    self._acc.execute_asset(self._sym, delta_position, 'BUY')

