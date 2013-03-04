# -*- coding: utf-8 -*-
import util
import yaml


class ConfigLoader(object):
  def __init__(self, config_file):
    self.filename = config_file
    if config_file:
      self.config = self.load_yaml(util.open_yaml(config_file))
    else:
      self.config = {}

  def load_yaml(self, content):
    """ string でも file でも同じメソッドで読みこめる """
    yaml_obj = list(yaml.load_all(content))
    return yaml_obj[0]

  def setup_klass(self, klasses):
    action_configs = self.config.get('actions', {})
    for name, klass in klasses.items():
      setup_method = type.__getattribute__(klass, 'setup')
      setup_method(action_configs.get(name, {}))

