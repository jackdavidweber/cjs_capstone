import python.code_to_gast.py_router as pr
import ast


def while_statement_to_gast(node):
    gast = {}
    gast["type"] = "whileStatement"
    gast["body"] = pr.node_to_gast(node.body)
    gast["test"] = pr.node_to_gast(node.test)
    return gast


def for_statement_to_gast(node):
    """
    Converts python for statements to gast
    Includes:
        ForRangeStatements: for i in range(0,10,1)
        ForOfStatements: for elem in [1,2,3]
    """
    if type(node.iter) == ast.Call:
        return for_range_statement_to_gast(node)
    else:
        return for_of_statement_to_gast(node)


def for_of_statement_to_gast(node):
    gast = {}
    gast["type"] = "forOfStatement"
    gast["init"] = pr.node_to_gast(node.target)
    gast["iter"] = pr.node_to_gast(node.iter)
    gast["body"] = pr.node_to_gast(node.body)
    return gast


def for_range_statement_to_gast(node):
    """
    Converts for statement of the structure for i in range() to gast
    Notes about functionality
        - only works with 2-3 range args
        - only works if arg nodes are of type ast.Num (in case of positives) or 
        ast.UnaryOp (in case of negatives). Does not work with vars.
    """
    gast = {}
    try:
        gast["type"] = "forRangeStatement"
        ast.dump(node)
        args = node.iter.args
        start_num = get_start_num(args)
        end_num = get_end_num(args)
        step_num = get_step_num(args)

        gast["init"] = for_range_statement_init_helper(node.target, start_num)
        gast["test"] = for_range_statement_test_helper(node.target, start_num,
                                                       end_num)
        gast["update"] = for_range_statement_update_helper(
            node.target, step_num)
        gast["body"] = pr.node_to_gast(node.body)

    except:
        gast = {"type": "error", "value": "unsupported"}

    return gast


def for_range_statement_init_helper(var_node, start_num):
    """
    Takes a node representing start of loop and the variable node.
    returns a gast node representing value for the init key in forRangeStatement gast
    Example: ast.parse("for i in range(0,10,2)")
        input: var_node = ast.Name(i), start_num = 10,
        output: {'type': 'varAssign', 'kind': 'let', 'varId': {'type': 'name', 'value': 'i'}, 'varValue': {'type': 'num', 'value': 0}}
    """

    gast = {}
    gast["type"] = "varAssign"
    gast["kind"] = "let"
    gast["varId"] = pr.node_to_gast(var_node)
    gast["varValue"] = num_to_gast(start_num)

    return gast


def for_range_statement_test_helper(var_node, start_num, end_num):
    """
    Takes a variable node, start node and end node. Returns gast node
    representing value for the test key in forRangeStatement gast
    Example: ast.parse("for i in range(0,10,2)")
        input: var_node = ast.Name(i), start_num = 10, end_num = 2
        output: {'type': 'binOp', 'left': {'type': 'name', 'value': 'i'}, 'op': '<', 'right': {'type': 'num', 'value': 10}}
    """

    # first need to figure out whether to use "<" or ">"
    if start_num <= end_num:
        op_str = "<"
    else:
        op_str = ">"

    gast = {}
    gast["type"] = "binOp"
    gast["left"] = pr.node_to_gast(var_node)
    gast["op"] = op_str
    gast["right"] = num_to_gast(end_num)

    return gast


def for_range_statement_update_helper(var_node, step_num):
    """
    takes a variable node and an integer that represents the step. Returns
    a gast node representing value for the update key in forRangeStatement gast
    Example: ast.parse("for i in range(0,10,2)")
        input: var_node = ast.Name(i), step_num = 2
        output: {'type': 'augAssign', 'left': {'type': 'name', 'value': 'i'}, 'op': '+=', 'right': {'type': 'num', 'value': 2}}
    """

    if step_num < 0:
        op_str = "-="
        right_gast = {
            "type": "num",
            "value": -1 * step_num  # FIXME: this feels very hacky
        }
    else:
        op_str = "+="
        right_gast = {"type": "num", "value": step_num}
    gast = {}
    gast["type"] = "augAssign"
    gast["left"] = pr.node_to_gast(var_node)
    gast["op"] = op_str
    gast["right"] = right_gast
    return gast


def get_step_num(args):
    """
    Gets step number based on arguments.
    Since gast is based on javascript AST, there must be 3 arguments for the 
    start, step and end. If only 2 args are provided, python assumes step=1.
    Any other number of arguments will result in an error.
    """

    if len(args) == 3:
        step_num = arg_node_to_num(args[2])

    elif len(args) == 2:
        step_num = 1

    elif len(args) == 1:
        step_num = 1

    else:
        return {"type": "error", "value": "unsupported"}

    return step_num


def get_start_num(args):
    if len(args) == 3 or len(args) == 2:
        return arg_node_to_num(args[0])

    elif len(args) == 1:
        return 0

    else:
        return {"type": "error", "value": "unsupported"}


def get_end_num(args):
    if len(args) == 3 or len(args) == 2:
        return arg_node_to_num(args[1])

    elif len(args) == 1:
        return arg_node_to_num(args[0])

    else:
        return {"type": "error", "value": "unsupported"}


def arg_node_to_num(arg):
    """
    python stores argument nodes as ast.UnaryOp for negative numbers and
    ast.Num for positive numbers. This function takes care of this.
    """

    if type(arg) == ast.UnaryOp:
        return -1 * arg.operand.n
    else:
        return arg.n


def num_to_gast(num):
    """
    takes a number and converts it to gast
    """
    gast = {"type": "num", "value": num}
    return gast
