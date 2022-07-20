import re

class Problem:
  operands = []
  operators = []
  result = ''

  def __init__(self,str):
    self.operands = re.split('\W+',str)
    self.operators = re.findall('[^\w\s]+',str)

  def check(self):
    if not self.operands or not self.operators: return False
    if len(self.operands) != 2 or len(self.operators) != 1: return False #change this to allow more than 2 operands
    return True

  def check_operators(self,allowed_op=('+','-','*','/')):
    for operator in self.operators:
      if operator not in allowed_op: return False
    return True

  def check_operands(self):
    for operand in self.operands:
      if not operand.isdigit(): return False
    return True

  def check_operands_size(self,max_digits=0):
    for operand in self.operands:
      if max_digits and len(operand) > max_digits: return False
    return True
  
  def __calc_result(self):
    try:
      operations = {
        '+': (lambda a,b : a + b),
        '-': (lambda a,b : a - b),
        '*': (lambda a,b : a * b),
        '/': (lambda a,b : a / b),
      }
      result = int(self.operands[0])
      for i,op in enumerate(self.operators,start=1):
        result = operations[op](result,int(self.operands[i]))
      self.result = str(result)
    except:
      self.result = ''

  def write_txt(self,with_result=False):
    fill = 2 + len(max(self.operands,key=len))
    if with_result:
      self.__calc_result()
      fill = max(fill,len(self.result))
    txt = []
    for i,num in enumerate(self.operands,start=-1):
      if i == -1:
        txt.append(num.rjust(fill,' '))
      else:
        txt.append(
          self.operators[i] +
          num.rjust(fill-1,' ')
        )
    txt.append(''.rjust(fill,'-'))
    if self.result: txt.append(self.result.rjust(fill,' '))

    return txt


class ProblemEx(Exception):
  msgs = [
    "Error: undefined",
    "Error: Too many problems.",
    "Error: Operator must be '+' or '-'.",
    "Error: Numbers must only contain digits.",
    "Error: Numbers cannot be more than four digits."
  ]
  i = 0
  
  def __init__(self, i):
    self.i = i
  
  def get_msg(self):
    return self.msgs[self.i]


def arithmetic_arranger(problems,with_results=False):
  matrix = []
  ret = ''

  try:
    if len(problems) > 5: raise ProblemEx(1)
    for problem_str in problems:

      pr = Problem(problem_str)
      if not pr.check(): raise ProblemEx(0)
      if not pr.check_operands(): raise ProblemEx(3)
      if not pr.check_operands_size(4): raise ProblemEx(4)
      if not pr.check_operators(('+','-')): raise ProblemEx(2)
      matrix.append(pr.write_txt(with_results))
    
    matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]  #transpose matrix
    lines = []
    for line in matrix:
      lines.append('    '.join(line))
    ret = '\n'.join(lines)

  except ProblemEx as e:
    ret = e.get_msg()
  except Exception as e:
    ret = e
  
  return ret
