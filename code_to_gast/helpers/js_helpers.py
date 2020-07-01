import js_router

"""
handles arrays and recursively calls node_to_gast on all its elements
"""
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
    gast (output): {'type': 'root', 'body': [{'type': 'funcCall', 'value': {'type': 'logStatement'}, 'args': [{'type': 'str', 'value': 'hello'}]}]}
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
      gast["left"] = js_router.node_to_gast(bop.left)
      gast["op"] = bop.operator
      gast["right"] = binOp(bop.right)
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
def memExp_to_gast(node):
  if node.property.name == "log":
    return {"type": "logStatement"}

  gast = {"type": "attribute", "id": node.property.name}
  gast["value"] = js_router.node_to_gast(node.object)
  return gast

"""
takes a node that represents a list of nodes.
returns a list of gast
example console.log("hello"):
    node (input):
    gast (output): [{'type': 'funcCall', 'value': {'type': 'logStatement'}, 'args': [{'type': 'str', 'value': 'hello'}]}]
example array of strings:
    input: [Str(s='hello'), Str(s='world')]
    output:[{'type': 'str', 'value': 'hello'}, {'type': 'str', 'value': 'world'}]
"""
def node_list(node):
    gast_list = []
    for i in range(0, len(node)):
        gast_list.append(js_router.node_to_gast(node[i]))
    return gast_list

"""
Seems like this block statement type is called
whenever there are curly braces. Probably will need 
to end up making this function more robust.
"""
def js_block_statement(node):
  return js_router.node_to_gast(node.body)


def unary_to_gast(node):
    return {"type": "unaryOp", "op": node.operator, "arg": js_router.node_to_gast(node.argument)}