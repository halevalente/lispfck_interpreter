import ox
import click
import pprint

lexer = ox.make_lexer ([
  ('LEFT_PARENTHESIS', r'\('),
  ('RIGHT_PARENTHESIS', r'\)'),
  ('LOOP', r'loop'),
  ('DECREMENT', r'dec'),
  ('INCREMENT', r'inc'),
  ('RIGHT', r'right'),
  ('LEFT', r'left'),
  ('PRINT', r'print'),
  ('READ', r'read'),
  ('ADD', r'add'),
  ('SUB', r'sub'),
  ('DO', r'do'),
  ('NUMBER', r'[0-9]+'),
  ('IGNORE_COMMENT', r';[^\n]*'),
  ('IGNORE_LINE_BREAK', r'\n'),
  ('IGNORE_SPACE', r'\s+')
])

tokens_list = [
  'LEFT_PARENTHESIS',
  'RIGHT_PARENTHESIS',
  'DECREMENT',
  'INCREMENT',
  'LOOP',
  'RIGHT',
  'LEFT',
  'READ',
  'PRINT',
  'ADD',
  'SUB',
  'DO',
  'NUMBER']

parser = ox.make_parser ([
  ('expr : LEFT_PARENTHESIS RIGHT_PARENTHESIS', lambda x,y: '()'),
  ('expr : LEFT_PARENTHESIS term RIGHT_PARENTHESIS', lambda x,y,z: y),
  ('term : atom term', lambda x,y: (x,) + y),
  ('term : atom', lambda x : (x,)),
  ('atom : expr', lambda x : x),
  ('atom : DECREMENT', lambda x : x),
  ('atom : INCREMENT', lambda x : x),
  ('atom : LOOP', lambda x : x),
  ('atom : RIGHT', lambda x : x),
  ('atom : LEFT', lambda x : x),
  ('atom : READ', lambda x : x),
  ('atom : PRINT', lambda x : x),
  ('atom : ADD', lambda x : x),
  ('atom : SUB', lambda x : x),
  ('atom : DO', lambda x : x),
  ('atom : NUMBER', int),
], tokens_list)