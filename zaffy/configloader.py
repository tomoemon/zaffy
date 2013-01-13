# -*- coding: utf-8 -*-
import yaml


class ConfigLoader(object):
  def __init__(self, config_file):
    self.filename = config_file
    if config_file:
      self.config = self.load_yaml(file(config_file))
    else:
      self.config = {}

  def load_yaml(self, content):
    """ string でも file でも同じメソッドで読みこめる """
    yaml_obj = list(yaml.load_all(content))
    return yaml_obj[0]

  def setup_klass(self, klasses):
    action_configs = self.config.get('actions', {})
    for name, klass in klasses.items():
      if name not in action_configs:
        continue
      setup_method = type.__getattribute__(klass, 'setup')
      setup_method(action_configs[name])

