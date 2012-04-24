# -*- coding: utf-8 -*-
import sys
import argparse
from actionloader import action_loader
from scenarioloader import scenario_loader

def main():
  action_loader.load_actions()
  global_env = {}
  global_env.update(action_loader.get_all_action_map())
  scenario = scenario_loader.load_file(sys.argv[1])
  scenario.run(global_env)

if __name__ == '__main__':
  main()
