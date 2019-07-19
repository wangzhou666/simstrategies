#!/usr/bin/env python3
from argparse import ArgumentParser
import account
import json
import quoteapi
import simulator
import strategy

_STRATEGIES = {
    'scaledetf': strategy.ScaledETFStrategy,
}

def main():
  parser = ArgumentParser(description='Run the simulator.')
  parser.add_argument('--config', '-c', dest='configs',
                      action='append', default=[])
  args = parser.parse_args()

  for filename in args.configs:
    run_with_config(filename)

def run_with_config(config_filename):
  with open(config_filename, 'r') as cf:
    config = json.load(cf)

  av_client = quoteapi.AlphaVantageClient(
      apikey=config['alphavantage_key'])
  acc = account.VirtualAccount(
      cash=config['account']['cash'])
  
  stg_name = config['strategy']['name']
  stg_kwargs = config['strategy']['kwargs']
  stg_cls = _STRATEGIES[stg_name]
  stg = stg_cls(**stg_kwargs)

  hst = {
      'daily_adjusted': av_client.load_daily_adjusted(
          symbol=config['history']['symbol'])
  }
  sim = simulator.DailyStrategySimulator(
      account=acc, strategy=stg, history=hst,
      start=config['history']['start'],
      end=config['history']['end'])

  sim.simulate()
  print(sim)


if __name__ == '__main__':
  main()

