import shared.gast_to_code.general_helpers as general_helpers
import shared.gast_to_code.gast_to_code_router as router
from shared.gast_to_code.error_handler import ErrorHandler


class BashGastToCodeConverter():
    name = "Bash"
    is_beta = True
    is_input_lang = False
    is_output_lang = True

    def __init__(self):
        self.error_handler = ErrorHandler()

    def get_error_handler(self):
        return self.error_handler

    def handle_bool(self, gast):
        return "Bash does not support booleans"

    def handle_log_statement(self, gast):
        return "echo"

    def handle_func_call(self, gast):
        return router.gast_to_code(gast["value"],
                                   "bash") + " " + bash_arg_helper(gast["args"])

    def handle_arr(self, gast):
        # This logic returns an error for nested arrays which are not supported in bash
        if general_helpers.arr_in_list(gast["elements"]):
            return self.error_handler.impossible_translation()

        return "(" + router.gast_to_code(gast["elements"], "py") + ")"

    def handle_if(self, gast, lvl=0):
        test = router.gast_to_code(gast["test"], "bash")
        body_indent = "\n\t" + "\t" * lvl
        closing_exp_indent = "\n" + "\t" * lvl
        body = general_helpers.list_helper(gast["body"], "bash", body_indent,
                                           lvl + 1)

        out = "if [[ " + test + " ]]; then" + body_indent + body + closing_exp_indent

        if len(gast["orelse"]) == 0:
            out += "fi"
        elif gast["orelse"][0]["type"] == "if":
            out += "el" + router.gast_to_code(gast["orelse"], "bash")
        else:
            out += "else\n\t" + general_helpers.list_helper(
                gast["orelse"], "bash", "\n\t") + "\nfi"

        return out

    def handle_var_assign(self, gast):
        value = router.gast_to_code(gast["varValue"], "bash")
        return router.gast_to_code(gast["varId"], "bash") + "=" + value

    def handle_aug_assign(self, gast):
        if "right" in gast:
            return router.gast_to_code(
                gast["left"],
                "bash") + " " + gast["op"] + " " + router.gast_to_code(
                    gast["right"], "bash")
        else:
            return router.gast_to_code(gast["left"], "bash") + gast["op"]

    def handle_name(self, gast):
        return gast["value"]


'''
Helper functions for bash converter since variables are written different when function params
These functions are called on func args only and return the correct translation
'''


def handle_var_arg(gast):
    return '"$' + gast["value"] + '"'


def bash_arg_helper(gast_list):
    out = ""
    for i in range(0, len(gast_list)):
        if gast_list[i]["type"] == "name":
            out += handle_var_arg(gast_list[i])
        else:
            out += router.gast_to_code(gast_list[i], "bash")

        if i < len(gast_list) - 1:  # don't add delimiter for last item
            out += " "
    return out
