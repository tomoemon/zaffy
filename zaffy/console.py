# -*- coding: utf-8 -*-
import sys
import cmd
import inspect
from pprint import pformat
from actionloader import action_loader
from scenarioloader import scenario_loader
from scenariosetting import ScenarioSetting
from baseaction import ActionException
from assertionfailed import AssertionFailed

class CUI(cmd.Cmd):
  prompt = ">>> "

  def __init__(self, global_env):
    cmd.Cmd.__init__(self)
    self.global_env = global_env
    self.scenario = None

    # cmd.Cmd クラスで do_hogehoge 関数を定義すると、
    # hogehoge コマンドを補完してくれる
    # 合わせて complete_hogehoge 関数を定義すると
    # hogehoge fuga と入力中に fuga の部分を補完してくれる
    setattr(CUI, "do_action: ", self._do_action)
    setattr(CUI, "complete_action:", self._complete_action)
    CUI.identchars += ':'
    self.action_complete = []
    self.action_param_complete = {}
    for action_name, action_klass in action_loader.get_all_action_map().items():
      for method in dir(action_klass):
        method_obj = getattr(action_klass, method)
        if method.startswith('do_') and callable(method_obj):
          args = inspect.getargspec(method_obj).args
          args = self.remove_item(args, ['self', 'scenario', 'global_env'])
          args.extend(["assert", "assertex"])
          method = method.replace('do_', '')

          if method == action_name:
            action_key = action_name
          else:
            action_key = action_name + '.' + method
          self.action_complete.append(action_key)
          self.action_param_complete[action_key] = args

  def precmd(self, line):
    """ >>> の状態で enter が押されて、do_hogehoge へのマッチングを行う前に呼ばれる """
    if hasattr(CUI, 'do_action: '):
      delattr(CUI, "do_action: ")
      setattr(CUI, "do_action:", self._do_action)
    return line

  def postcmd(self, stop, line):
    """ do_hogehoge (or default) が終わった後に呼ばれる """
    if hasattr(CUI, 'do_action:'):
      delattr(CUI, "do_action:")
      setattr(CUI, "do_action: ", self._do_action)

  @staticmethod
  def remove_item(item_list, remove_items):
    for remove_item in remove_items:
      try:
        item_list.remove(item)
      except:
        pass
    return item_list

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

  def action_hook(func):
    """ decorator function """
    def wrapper(self, param):
      delattr(CUI, "do_action:")
      self.set_param_complete(param)
      func(self, param)
      self.delete_param_complete(param)
      setattr(CUI, "do_action: ", self._do_action)
    return wrapper

  @action_hook
  def _do_action(self, param):
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
    except AssertionFailed as e:
      print(e.__class__.__name__)
      print(e.__dict__)
      self.scenario.finished_action_count += 1
    except ActionException as e:
      print(e.original.__class__.__name__)
      print(e.original)
      self.scenario.finished_action_count += 1
    except Exception as e:
      print(e.__class__.__name__)
      print(e)
    sys.stdout.write("\n")

  def set_param_complete(self, action_key):
    if action_key in self.action_param_complete:
      for param_name in self.action_param_complete[action_key]:
        setattr(CUI, "do_" + param_name + ': ', lambda x=0: x)

  def delete_param_complete(self, action_key):
    if action_key in self.action_param_complete:
      for param_name in self.action_param_complete[action_key]:
        delattr(CUI, "do_" + param_name + ': ')

  def _complete_action(self, *args):
    return [a for a in self.action_complete if a.startswith(args[1].split()[1])]

def run(global_env):
  CUI(global_env).cmdloop()

if __name__ == '__main__':
  action_loader.load_actions()
  run({})

