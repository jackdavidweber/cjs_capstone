import javascript.code_to_gast.js_assign as js_assign
import javascript.code_to_gast.js_expression as js_expression
import javascript.code_to_gast.js_conditional as js_conditional
import javascript.code_to_gast.js_loop as js_loop
import javascript.code_to_gast.js_helpers as js_helpers
import esprima


def node_to_gast(node):
    """
    # TODO: add whitespace
    Takes js and converts to generic ast node
    """
    #  check if list before calling type to avoid error
    if type(node) == list:
        return js_helpers.node_list(node)
    # base cases
    if node.type == "Literal":
        # must check bool first since bool is instance of int
        if isinstance(node.value, bool):
            if node.raw == "true":
                node.value = 1
            else:
                node.value = 0
            return {"type": "bool", "value": node.value}
        elif isinstance(node.value, int):
            return {"type": "num", "value": node.value}
        elif isinstance(node.value, str):
            return {"type": "str", "value": node.value}
        elif node.raw == "null":
            return {"type": "none"}
        else:
            return {"type": "error", "value": "unsupported"}
    elif node.type == "BreakStatement":
        return {"type": "break"}
    elif node.type == "ContinueStatement":
        return {"type": "continue"}
    elif node.type == "Identifier":
        # identifier has quotes around name
        return {"type": "name", "value": node.name}
    elif node.type == "BinaryExpression":
        return js_helpers.bin_op_to_gast(node)
    elif node.type == "LogicalExpression":
        return js_helpers.bool_op_to_gast(node)
    elif node.type == "UnaryExpression":
        return js_helpers.unary_to_gast(node)
    elif node.type == "UpdateExpression":
        return js_helpers.update_expression_to_gast(node)
    #statements
    elif node.type == "VariableDeclaration":
        return js_assign.assign_to_gast(node)
    elif node.type == "AssignmentExpression":
        return js_assign.aug_assign_to_gast(node)
    elif node.type == "ExpressionStatement":
        return js_expression.convert_expression_to_gast(node)
    elif node.type == "CallExpression":
        return js_expression.call_expression_to_gast(node)
    elif node.type == "MemberExpression":
        return js_expression.member_expression_to_gast(node)
    elif node.type == "Program":
        return js_helpers.program_to_gast(node)
    elif node.type == "ArrayExpression":
        return js_helpers.array_expression_to_gast(node)
    elif node.type == "ObjectExpression":
        return js_helpers.dictionary_to_gast(node)
    elif node.type == "Property":
        return js_helpers.property_to_gast(node)
    elif node.type == "BlockStatement":
        return js_helpers.block_statement_to_gast(node)
    # Conditionals
    elif node.type == "IfStatement":
        return js_conditional.if_statement_to_gast(node)
    # functions
    elif node.type == "FunctionDeclaration":
        return js_expression.func_declarations_to_gast(node)
    elif node.type == "ReturnStatement":
        return js_helpers.return_statement_to_gast(node)
    elif node.type == "AssignmentPattern":
        return js_helpers.assign_pattern_to_gast(node)
    elif node.type == "ArrowFunctionExpression":
        return js_expression.arrow_function_to_gast(node)
    elif node.type == "FunctionExpression":
        return js_expression.arrow_function_to_gast(node)
    # Loops
    elif node.type == "WhileStatement":
        return js_loop.while_statement_to_gast(node)
    elif node.type == "ForStatement":
        return js_loop.for_range_statement_to_gast(node)
    elif node.type == "ForOfStatement":
        return js_loop.for_of_statement_to_gast(node)
    else:
        # not supported
        return {"type": "error", "value": "unsupported"}
