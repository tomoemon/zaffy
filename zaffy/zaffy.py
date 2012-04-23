# -*- coding: utf-8 -*-
import sys
from scenarioloader import ScenarioLoader
from actionloader import action_loader

def main():
  global_env = {}
  global_env.update(action_loader.get_all_action_map())
  loader = ScenarioLoader()
  scenario = loader.load_file(sys.argv[1])
  scenario.run(global_env)

if __name__ == '__main__':
  main()
