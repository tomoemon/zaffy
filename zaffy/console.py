# -*- coding: utf-8 -*-
import sys
import cmd
from pprint import pformat
from actionloader import action_loader
from scenarioloader import scenario_loader
from scenariosetting import ScenarioSetting
from baseaction import ActionException

class CUI(cmd.Cmd):
  prompt = ">>> "

  def __init__(self, global_env):
    cmd.Cmd.__init__(self)
    self.global_env = global_env
    self.scenario = None

    setattr(CUI, "do_action:", self._do_action)
    setattr(CUI, "complete_action:", self._complete_action)
    CUI.identchars += ':'
    self.actions = []
    for action_name, action in action_loader.get_all_action_map().items():
      for method in dir(action):
        if method.startswith('do_'):
          method = method.replace('do_', '')
          if method == action_name:
            continue
          self.actions.append(action_name + '.' + method)

  def do_exit(self, line):
    return 1

  def default(self, line):
    try:
      result = eval(line, self.global_env)
      sys.stdout.write(pformat(result, indent=2))
    except Exception as e:
      sys.stdout.write(unicode(e))
    sys.stdout.write("\n\n")

  def run_scenario(self, lines):
    lines = ['  ' + line for line in lines]
    lines.insert(0, '- ')
    lines.insert(0, '- zaffy repl scenario')
    raw_str = "\n".join(lines)
    setting = ScenarioSetting(body=raw_str)
    new_scenario = scenario_loader.load(setting)
    if not self.scenario:
      self.scenario = new_scenario
      self.scenario.run(self.global_env)
    else:
      self.scenario.add_action(new_scenario.actions[0])
      self.scenario.run(self.global_env)

  def _do_action(self, param):
    delattr(CUI, "do_action:")
    lines = ["action: {0}".format(param)]
    while True:
      line = raw_input("... ").rstrip()
      if not line:
        # run action
        break
      elif line == '\c':
        return
      lines.append(line)
    try:
      self.run_scenario(lines)
    except ActionException as e:
      print(e.original.__class__.__name__)
      print(e.original)
      self.scenario = None
    except Exception as e:
      print(e.__class__.__name__)
      print(e)
      self.scenario = None
    sys.stdout.write("\n")
    setattr(CUI, "do_action:", self._do_action)

  def _complete_action(self, *args):
    return [a for a in self.actions if a.startswith(args[1].split()[1])]

def run(global_env):
  CUI(global_env).cmdloop()

if __name__ == '__main__':
  action_loader.load_actions()
  run({})

