# -*- coding: utf-8 -*-
from baseaction import ActionException
import six
from debugprinter import DebugPrinter


class ScenarioDoc(object):
  def __init__(self, raw_doc):
    if isinstance(raw_doc, six.string_types):
      self.doc = raw_doc
      self.tags = []
    elif isinstance(raw_doc, dict):
      self.doc = raw_doc['doc']
      tag = raw_doc.get('tag', [])
      self.tags = tag if isinstance(tag, list) else [tag]
    else:
      raise Exception('unexpected scenario document')


class Scenario(object):
  def __init__(self, setting, doc, actions, parent=None):
    self.setting = setting
    self.doc = doc
    self.parent = parent
    self.localvar = {}

    self._action_queue = actions
    self._finished_actions = []

  def __getattr__(self, item):
    return getattr(self.setting, item)

  @property
  def queue(self):
    return self._action_queue

  @property
  def actions(self):
    return self._finished_actions

  @property
  def action_index(self):
    return len(self._finished_actions)

  def run(self, global_env):
    # 一時対応
    if not self.parent:
      type.__getattribute__(global_env["const"], 'init_scenario')()
      type.__getattribute__(global_env["preset"], 'init_scenario')()
    # ここまで

    global_env["scenario"] = self
    global_env["local"] = self.localvar
    global_env["debugprinter"] = DebugPrinter(global_env['formatter'], self)

    while self._action_queue:
      self.run_action(global_env)

    if self.parent:
      global_env["scenario"] = self.parent
      global_env["local"] = self.parent.localvar

  def add_action(self, action):
    self._action_queue.append(action)

  def run_action(self, global_env):
    action = self._action_queue.pop(0)

    global_env["actions"] = self.actions
    global_env["action_index"] = self.action_index
    global_env["this"] = action
    global_env["last"] = self.actions[-1] if self.actions else None
    try:
      action.run_action(global_env)
    except ActionException as e:
      e.action_index = self.action_index
      e.scenario = self
      raise
    finally:
      action.debug_print(global_env['debugprinter'], self.action_index)
      self.actions.append(action)

