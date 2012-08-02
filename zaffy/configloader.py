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

  def apply_config_to_klass(self, klasses):
    action_config = self.config.get('actions', {})
    for name, klass in klasses.items():
      if name in action_config:
        type.__getattribute__(klass, 'apply_config')(action_config[name])

