class Strategy(object):
  def apply(self, account):
    raise NotImplementedError()


class ScaledETFStrategy(Strategy):
  def __init__(
      self, symbol, amplifier=1, **kwargs):
    self._sym = symbol
    self._amp = amplifier
    self._kwargs = kwargs

  def __str__(self):
    tmpl = (
        'Scaled ETF strategy:\n'
        ' - Tracking symbol: %s\n'
        ' - Amplifier: %s')
    return tmpl % (self._sym, self._amp)

  @property
  def symbol(self):
    return self._sym

  def apply(self, account):
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
    assets = account.list_assets()
    for ast in assets:
      if ast.symbol == self._sym: continue
      account.execute_asset(ast.symbol, ast.position, 'SELL')

    tgt_cash = (1 - self._amp) * account.get_net_value()
    spending_cash = account.cash - tgt_cash
    delta_position = spending_cash / account.get_asset(self._sym).close
    if not self._kwargs.get('allow_float_position'):
      delta_position = int(delta_position)
    account.execute_asset(self._sym, delta_position, 'BUY')

