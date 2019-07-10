from argparse import ArgumentParser
import json


def main():
  parser = ArgumentParser(description='Run the simulator.')
  parser.add_argument('--config_file', '-c', dest='config')
  args = parser.parse_args()

  with open(args.config, 'r') as cf:
    config = json.load(cf)


if __name__ == '__main__':
  main()

