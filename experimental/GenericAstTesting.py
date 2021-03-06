import astor
import ast
import json


# Takes source code and returns generic AST
def pythonToAst(filename):
  pythonToGenericAst = {'print':'logStatement'}
  srcAst = astor.code_to_ast.parse_file(filename)
  body = srcAst.body
  print(astor.dump_tree(srcAst))

  convertedAst = {'type': 'root', 'body': []}
  for statement in body:
    if type(statement) == ast.Expr:
      convertedAst['body'].append(handleExpression(statement, pythonToGenericAst))
    if type(statement) == ast.Assign:
      convertedAst['body'].append(handleAssign(statement))
  return convertedAst

#Helper function to convert expressions
def handleExpression(statement, pythonToGenericAst):
  if type(statement.value) == ast.Call:
    func = statement.value.func
    args = statement.value.args[0]
    if type(func) == ast.Name:
      return {'type': pythonToGenericAst[func.id], 'args': [args.s]}

#Helper function to convert declarations
def handleAssign(statement):
  if type(statement.targets[0]) == ast.Name:
    val = statement.value
    if type(val) == ast.Num:
      return {'type': 'varAssign', 'varId': statement.targets[0].id, 'varValue': val.n}
    if type(val) == ast.Str:
      return {'type': 'varAssign', 'varId': statement.targets[0].id, 'varValue': val.s}
    if type(val) == ast.List:
      return {'type': 'varAssign', 'varId': statement.targets[0].id, 'varValue': val.elts}

# Takes generic AST and returns Python source code
def astToPython(genericAst):
  genericAstToPython = {'logStatement': 'print'}
  outputPython = ''
  for statement in genericAst['body']:
    if statement['type'] == 'logStatement':
      outputPython += genericAstToPython[statement['type']]
      outputPython += '(\'' + statement['args'][0] + '\')\n'
    elif statement['type'] == 'varAssign':
      if type(statement['varValue']) == list:
        outputPython += statement['varId'] + ' = ' + '[]' + '\n'  
      elif type(statement['varValue']) == str:
        outputPython += statement['varId'] + ' = \'' + str(statement['varValue']) + '\'\n'
      else:
        outputPython += statement['varId'] + ' = ' + str(statement['varValue']) + '\n'
  #Get rid of last \n character
  return outputPython[:-1]

# Translates from Python to Generic AST and back to Python
def codeTranslate(filename):
  genericAst = pythonToAst(filename)
  return astToPython(genericAst)

#print(pythonToAst('ExamplePythonFile.py'))
#json = json.load(open('ExampleJson.json'))
#print(astToPython(json))