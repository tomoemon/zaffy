# -*- coding: utf-8 -*-
import yaml
import sys

def load_yaml():
  return yaml.load_all(file(sys.argv[1]))

def main():
  print len(list(load_yaml()))
  for doc in load_yaml():
    print doc

if __name__ == '__main__':
  main()
