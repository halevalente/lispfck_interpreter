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

