# -*- coding: utf-8
import yaml
from scenario import Scenario, ScenarioDoc
from actionloader import action_loader
from yaml.composer import Composer
from yaml.constructor import Constructor


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
      return content[0], content[1] if isinstance(content[1], list) else []
    else:
      return content[0][0], content[0][1:]

  def parse(self, raw_yaml):
    #add hooks to compose_node and construct_mapping
    #save the line number into __line__
    loader = yaml.Loader(raw_yaml)
    def compose_node(parent, index):
      line = loader.line
      node = Composer.compose_node(loader, parent, index)
      node.__line__ = line + 1
      return node
    def construct_mapping(node, deep=False):
      mapping = Constructor.construct_mapping(loader, node, deep=deep)
      mapping['__line__'] = node.__line__
      return mapping
    def load_all():
      try:
        while loader.check_data():
          yield loader.get_data()
      finally:
        loader.dispose()
    loader.compose_node = compose_node
    loader.construct_mapping = construct_mapping
    loader.load_all = load_all
    content = list(loader.load_all())

    raw_doc, raw_actions = self._filter(content)
    try:
      doc = ScenarioDoc(raw_doc)
    except:
      raise Exception("Scenario should have a description at first element/document: " + str(content))
    return doc, raw_actions

  def create_actions(self, actions):
    result = []
    for action in actions:
      result.append(action_loader.create_action(action))
    return result


scenario_loader = ScenarioLoader()

