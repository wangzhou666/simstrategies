import bisect

class DailyStrategySimulator(object):
  def __init__(self, account, strategy, history,
               start, end):
    self._acc = account
    self._stg = strategy
    self._hst = history
    assert start <= end
    self._date_range = str(start), str(end)

  def __str__(self):
    tmpl = (
        '---------------------\n'
        'From %s To %s\n'
        '%s\n'
        '%s')
    sd, ed = self._date_range
    return tmpl % (sd, ed, self._acc, self._stg)

  @property
  def account(self):
    return self._acc

  #TODO: deal with situation where multiple assets exist.
  def simulate(self):
    daily_adj_hst = self._hst['daily_adjusted']
    start, end = self._date_range

    dates = sorted(daily_adj_hst.keys())
    i = bisect.bisect_left(dates, start)
    j = bisect.bisect_right(dates, end)
    exp_dates = dates[i:j]

    symbol = self._stg.symbol
    for day in exp_dates:
      quote = float(daily_adj_hst[day]['5. adjusted close'])
      self._acc.update_asset_quote(symbol, quote)
      self._stg.apply(self._acc)

