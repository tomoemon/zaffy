# -*- coding: utf-8
import yaml
from scenario import Scenario, ScenarioDoc
from actionloader import action_loader


class ScenarioLoader(object):

  def _assert_no_circular_reference(self, filename, parent):
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
      self._assert_no_circular_reference(setting.filename, parent)

    doc, raw_actions = self.parse(setting.read())
    return Scenario(
        setting,
        doc,
        self.create_actions(raw_actions),
        parent)

  def _filter(self, content):
    if len(content) >= 2:
      return content[0], content[1]
    else:
      return content[0][0], content[0][1:]

  def parse(self, raw_yaml):
    content = list(yaml.load_all(raw_yaml))
    raw_doc, raw_actions = self._filter(content)
    try:
      doc = ScenarioDoc(raw_doc)
    except:
      raise Exception("Scenario should have a description at first element: " + str(content))
    return doc, raw_actions

  def create_actions(self, actions):
    result = []
    for action in actions:
      result.append(action_loader.create_action(action))
    return result


scenario_loader = ScenarioLoader()

