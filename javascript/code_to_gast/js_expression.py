import javascript.code_to_gast.js_helpers as js_helpers
import javascript.code_to_gast.js_router as js_router
import js_built_in_functions as built_in
"""
parses through top level expression 
"""


def convert_expression_to_gast(node):
    return js_router.node_to_gast(node.expression)


"""
takes python ast call node and converts to generic ast format
example print('hello'):
    exampleIn Call(func=Name(id='print'), args=[Str(s='hello')], keywords=[])
    exampleOut {'type': 'funcCall', 'value': {'type': 'logStatement'}, 'args': [{'type': 'str', 'value': 'hello'}]}
"""


def call_expression_to_gast(node):
    gast = {}
    gast["type"] = "funcCall"
    gast["value"] = js_router.node_to_gast(node.callee)
    gast["args"] = js_router.node_to_gast(node.arguments)
    return gast


def func_declarations_to_gast(node):
    gast = {}
    gast["type"] = "functionDeclaration"
    gast["id"] = js_router.node_to_gast(node.id)
    gast["params"] = js_router.node_to_gast(node.params)
    gast["body"] = js_router.node_to_gast(node.body)
    return gast


"""
Converts Member Expression to our generic AST recursively
Used for functions called on objects and std funcs like console.log
"""


def member_expression_to_gast(node):
    if node.computed == True:
        return subscript_to_gast(node)

    if node.object.name == "console" and node.property.name == "log":
        return {"type": "logStatement"}

    gast = {"value": js_router.node_to_gast(node.object)}
    func_name = node.property.name
    # The tool only currently supports the built in functions below
    # TODO add other built in function translations
    if func_name in {func.name for func in built_in.js_built_in_functions}:
        gast["type"] = "builtInAttribute"
        gast["id"] = built_in.js_built_in_functions[func_name].value
        return gast

    gast["type"] = "attribute"
    gast["id"] = node.property.name
    return gast


def subscript_to_gast(node):
    gast = {"type": "subscript"}
    gast["index"] = js_router.node_to_gast(node.property)
    gast["value"] = js_router.node_to_gast(node.object)
    return gast
