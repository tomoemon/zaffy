# -*- coding: utf-8 -*-
import sys
import cmd

actions = [
  "http.get",
  "http.post",
  "sql.update",
  "sql.select",
]

class CUI(cmd.Cmd):
    prompt = ">>> "
    def do_EOF(self, args):
        self.stdout.write("Exit!\n")
        return 1

    def default(self, line):
      self.stdout.write("unknown hoge: {0}\n".format(line))

def do_action(self, param):
  lines = ["action: {0}".format(param)]
  while True:
    line = raw_input("... ").rstrip()
    if not line:
      break
    lines.append(line)
  self.stdout.write("  " + "\n  ".join(lines) + "\n")

setattr(CUI, "do_action:", do_action)
setattr(CUI, "complete_action:", lambda self, *args: [a for a in actions if a.startswith(args[1].split()[1])])

CUI.identchars += ':'

CUI().cmdloop()
