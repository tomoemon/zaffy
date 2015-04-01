# -*- coding: utf-8 -*-
import re


class ActionSetting(object):

  ACTION_REGEX = re.compile(r'^(?P<actionName>\w+)(?:\.(?P<methodName>\w+))?(?:\s*(?P<presetMode>\<\<?)\s*(?P<presetName>\w+))?$')

  def __init__(self, raw_obj):
    if 'action' not in raw_obj or not raw_obj['action']:
      raise Exception("No action specified")

    match_dict = self._parse_action_id(raw_obj['action'])
    action_name = match_dict['actionName']
    method_name = match_dict['methodName']
    preset_mode = match_dict['presetMode']
    preset_name = match_dict['presetName']
    line_number = raw_obj['__line__']

    # action: http.get
    # の場合は http アクションの get メソッドを呼ぶ
    # action: require
    # のように . 付きでメソッドを明示しない場合は
    # メソッド名はアクションと同じになる
    if not method_name:
      method_name = action_name

    self.action_name = action_name
    self.method_name = method_name
    self.is_merge_preset = True if preset_mode == '<<' else False
    self.preset_name = preset_name
    self.line_number = line_number

    del raw_obj['action']
    del raw_obj['__line__']

    self.params = dict(raw_obj)

  def _parse_action_id(self, raw_action_id):
    match = self.ACTION_REGEX.match(raw_action_id)
    if match is None:
      raise Exception("Invalid action: '" + raw_action_id + "'")
    return match.groupdict()

