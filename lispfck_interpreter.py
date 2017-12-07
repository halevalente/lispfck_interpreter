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
  ('DO_AFTER', r'do-after'),
  ('DO_BEFORE', r'do-before'),
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
  'DO_AFTER',
  'DO_BEFORE',
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
  ('atom : DO_AFTER', lambda x : x),
  ('atom : DO_BEFORE', lambda x : x),
  ('atom : NUMBER', int),
], tokens_list)


def lispfck_interpreter(tree, initialArray, aux):
  loopIsActive = False
  pos = 0
  while pos < len(tree):
    if isinstance(tree[pos], tuple):
      initialArray, aux = lispfck_interpreter(tree[pos], initialArray, aux)
    elif tree[pos] == 'inc':
      initialArray[aux] += 1
    elif tree[pos] == 'dec':
      initialArray[aux] -= 1
    elif tree[pos] == 'right':
      aux += 1
      if len(initialArray) - 1 < aux:
        initialArray.append(0)
    elif tree[pos] == 'left':
      aux -= 1
      if aux < 0:
        initialArray.append(0)
    elif tree[pos] == 'add':
      pos += 1
      initialArray[aux] += tree[pos]
    elif tree[pos] == 'sub':
      pos += 1
      initialArray[aux] -= tree[pos]
    elif tree[pos] == 'read':
      initialArray[aux] = input('input: ')
    elif tree[pos] == 'print':
      print(chr(initialArray[aux]), end='')
    elif tree[pos] == 'do-before':
      pos += 1 # pass to command
      command = tree[pos]
      pos += 1 # pass to tuple
      array = do_before(command, list(tree[pos]))
      lispfck_interpreter(array, initialArray, aux)
    elif tree[pos] == 'do-after':
      pos += 1 # pass to command
      command = tree[pos]
      pos += 1 # pass to tuple
      array = do_after(command, list(tree[pos]))
      lispfck_interpreter(array, initialArray, aux)
    elif tree[pos] == 'loop':
      if initialArray[aux] == 0:
        loopIsActive = False
        break
      else:
        loopIsActive = True
    if loopIsActive == True and pos == len(tree) - 1:
      pos = -1

    pos += 1

  return initialArray, aux


def evaluate(tree):
  initialArray = [0]
  aux = 0
  print('\nOutput:')
  initialArray, aux = lispfck_interpreter(tree, initialArray, aux)
  print()

@click.command()
@click.argument('source', type=click.File('r'))


def do_before(command, previousArray):
  actualArray = []
  pos = 0
  while pos < len(previousArray):
    actualArray.append(command)
    actualArray.append(previousArray[pos])
    if previousArray[pos] == 'add' or previousArray[pos] == 'sub':
      pos += 1
      actualArray.append(previousArray[pos])

    pos += 1

  return actualArray


def do_after(command, previousArray):
  actualArray = []
  pos = 0
  while pos < len(previousArray):
    if previousArray[pos] == 'add' or previousArray[pos] == 'sub':
      actualArray.append(previousArray[pos])
      pos += 1
    actualArray.append(previousArray[pos])
    actualArray.append(command)

    pos += 1

  return actualArray


def build_tree(source):
  sourceCode = source.read()
  tokens = lexer(sourceCode)
  print('Tokens List:\n', tokens)
  tree = parser(tokens)
  print("\nSyntax Tree:")
  pprint.pprint(tree)
  evaluate(tree)

if __name__ == '__main__':
  build_tree()