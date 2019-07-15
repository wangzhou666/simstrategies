from argparse import ArgumentParser
import account
import json
import quoteapi
import simulator
import strategy

def main():
  #TODO: support batch run experiments.
  #TODO: support customized strategies
  parser = ArgumentParser(description='Run the simulator.')
  parser.add_argument('--config_file', '-c', dest='config')
  args = parser.parse_args()

  with open(args.config, 'r') as cf:
    config = json.load(cf)

  av_client = quoteapi.AlphaVantageClient(
      apikey=config['alphavantage_key'])
  acc = account.VirtualAccount(
      cash=config['account']['cash'])
  stg = strategy.ScaledETFStrategy(
      symbol=config['strategy']['symbol'],
      amplifier=config['strategy']['scale'],
      allpw_float_position=config['strategy'].get('allow_float_position'))
  hst = {'daily_adjusted': av_client.load_daily_adjusted(symbol=config['strategy']['symbol'])}
  sim = simulator.DailyStrategySimulator(
      account=acc, strategy=stg, history=hst,
      start=config['date']['start'], end=config['date']['end'])

  sim.simulate()
  print(sim)


if __name__ == '__main__':
  main()

