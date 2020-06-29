import js_router

#TODO: handling of booleans (have type literal)
def jsarg_to_str(arg):
  if arg.type == "Literal":
    return arg.value
  elif arg.type == "Identifier":
    #identifier has quotes around name
    return arg.name
  elif arg.type == "BinaryExpression":
    return binOp_to_str(arg)
  elif arg.type == "ArrayExpression":
    arg_list = []
    for elm in arg.elements:
        arg_list.append(jsarg_to_str(elm))
    return arg_list
  else:
    return ""

def js_array_expression(node):
    gast = {"type" : "arr"}
    gast["elts"] = []
    for elm in node.elements:
        gast["elts"].append(js_router.node_to_gast(elm))
    return gast
"""
takes ast node of type program and returns
a generic ast for that node
example print("hello"):
    node (input): Program(body=[ExpressionStatement(value=Call(func=Name(id='print'), args=[Str(s='hello')], keywords=[]))])
    gast (output): {'type': 'root', 'body': [{'type': 'logStatement', 'args': ['hello']}]}
"""
def program_to_gast(node):
    gast = {"type": "root"}
    gast["body"] = js_router.node_to_gast(node.body)
    return gast

"""
converts a python ast BinOp and converts it to a gast node
"""
def binOp(bop):
  gast = {"type" : "binOp"}
  if bop.left.type != "BinaryExpression" and bop.right.type != "BinaryExpression":
      gast["left"] = js_router.node_to_gast(bop.left)
      gast["op"] = bop.operator
      gast["right"] = js_router.node_to_gast(bop.right)
  if bop.left.type == "BinaryExpression":
      gast["left"] = binOp(bop.left)
      gast["op"] = bop.operator
      gast["right"] = js_router.node_to_gast(bop.right)
  if bop.right.type == "BinaryExpression":
      gast["left"] = binOp(bop.left)
      gast["op"] = bop.operator
      gast["right"] = js_router.node_to_gast(bop.right)
  return gast

# TODO: address gharel comment https://github.com/jackdavidweber/cjs_capstone/pull/32#discussion_r446407392
def boolOp(node):
    gast = {"type": "boolOp"}
    if node.left.type != "LogicalExpression" and node.right.type != "LogicalExpression":
        gast["left"] = js_router.node_to_gast(node.left)
        gast["op"] = node.operator
        gast["right"] = js_router.node_to_gast(node.right)
    elif node.left.type == "LogicalExpression":
        gast["left"] = boolOp(node.left)
        gast["op"] = node.operator
        gast["right"] = js_router.node_to_gast(node.right)
    elif node.right.type == "LogicalExpression":
        gast["left"] = js_router.node_to_gast(node.left)
        gast["op"] = node.operator
        gast["right"] = boolOp(node.right)
    return gast

"""
Converts Member Expression and converts to readable string recursively
Used for functions called on objects and std funcs like console.log
"""
def memExp(node):
  if node.property.name == "log":
    return {"type": "logStatement"}

  gast = {"type": "attribute", "id": node.property.name}
  gast["value"] = js_router.node_to_gast(node.object)
  return gast

"""
takes list of arguments in js ast and converts them to a list of
strings
"""
def jsargs_to_strlist(args):
  out = []
  for arg in args:
    out.append(jsarg_to_str(arg))
  return out

"""
takes a node that represents a list of nodes.
returns a list of gast
example console.log("hello"):
    node (input):
    gast (output): [{'type': 'logStatement', 'args': ['hello']}]
example array of strings:
    input: [Str(s='hello'), Str(s='world')]
    output:['hello', 'world']
"""
def node_list(node):
    gast_list = []
    for i in range(0, len(node)):
        gast_list.append(js_router.node_to_gast(node[i]))
    return gast_list
