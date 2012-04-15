# -*- coding: utf-8 -*-
import sys
from scenarioloader import ScenarioLoader


def main():
  global_env = {}
  loader = ScenarioLoader()
  scenario = loader.load(sys.argv[1])
  scenario.run(global_env)

if __name__ == '__main__':
  main()
