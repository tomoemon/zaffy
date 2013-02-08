# -*- coding: utf-8
import yaml
from scenario import Scenario
from actionloader import action_loader


class ScenarioLoader(object):

  def _check_circular_reference(self, filename, parent):
    """ 循環参照チェック """
    refer_list = [filename]
    while parent:
      from_filename = parent.filename
      if from_filename in refer_list:
        refer_list.append(from_filename)
        raise Exception("Circular reference detected: " + str(list(reversed(refer_list))))
      refer_list.append(from_filename)
      parent = parent.parent

  def load(self, setting, parent=None):
    if setting.filename and parent:
      self._check_circular_reference(setting.filename, parent)

    raw_scenario = list(yaml.load_all(setting.read()))
    doc, raw_actions = self._parse(raw_scenario)

    return Scenario(
        setting,
        doc,
        self.create_actions(raw_actions),
        parent)

  def _parse(self, content):
    raw_actions = content[0]
    doc = raw_actions.pop(0)
    if not isinstance(doc, basestring):
      raise Exception("Scenario should have a description at first element: " + str(content))
    return doc, raw_actions

  def create_actions(self, actions):
    result = []
    for action in actions:
      result.append(action_loader.create_action(action))
    return result


scenario_loader = ScenarioLoader()

