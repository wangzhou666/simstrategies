import bisect
import re

class DailyStrategySimulator(object):
  def __init__(self, account, strategy, history,
               start, end):
    self._acc = account
    self._stg = strategy
    self._hst = history
    self._date_range = (start, end)

    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    assert all(
        date_pattern.match(d) for d in self._date_range)
    assert start <= end

  @property
  def account(self):
    return self._acc

  # TODO: deal with situation where multiple assets exist.
  def simulate(self):
    daily_adj_hst = self._hst['daily_adjusted']
    start, end = self._date_range

    dates = sorted(daily_adj_hst.keys())
    i = bisect.bisect_left(dates, start)
    j = bisect.bisect_right(dates, end)
    exp_dates = dates[i:j]

    symbol = self._stg.symbol
    for day in exp_dates:
      self._acc.update_asset_quote(
          symbol, daily_adj_hst[day]['5. adjusted close'])
      self._stg.apply(self._acc)

