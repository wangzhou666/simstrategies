class DailyStrategySimulator(object):
  def __init__(self, account, strategy, history,
               start, end):
    self._acc = account
    self._stg = strategy
    self._hst = history
    self._date_range = (start, end)

