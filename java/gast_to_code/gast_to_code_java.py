import shared.gast_to_code.gast_to_code_router as router
import shared.gast_to_code.general_helpers as general_helpers
import java.gast_to_code.java_helpers as java_helpers
from shared.gast_to_code.error_handler import ErrorHandler


class JavaGastToCodeConverter():
    name = "Java"
    is_beta = True
    is_input_lang = True
    is_output_lang = True

    def __init__(self):
        self.error_handler = ErrorHandler()

    def get_error_handler(self):
        return self.error_handler


    def handle_bool(self, gast):
        if gast["value"] == 1:
            return "true"
        else:
            return "false"

    def handle_if(self, gast, lvl=0):
        test = router.gast_to_code(gast["test"], "java")
        body_indent = "\n\t" + "\t" * lvl
        closing_brace_indent = "\n" + "\t" * lvl
        body = general_helpers.list_helper(gast["body"], "java", body_indent,
                                           lvl + 1)

        out = 'if (' + test + ') {' + body_indent + body + closing_brace_indent + "}"

        if len(gast["orelse"]) == 0:
            pass
        elif gast["orelse"][0]["type"] == "if":
            out += " else " + router.gast_to_code(gast["orelse"], "java")
        else:
            out += " else {\n\t" + general_helpers.list_helper(
                gast["orelse"], "java", "\n\t") + "\n}"

        return out

    def handle_none(self, gast):
        return "null"

    def handle_while(self, gast, lvl=0):
        test = router.gast_to_code(gast["test"], "java")

        body_indent = "\n\t" + "\t" * lvl
        closing_brace_indent = "\n" + "\t" * lvl
        body = general_helpers.list_helper(gast["body"], "java", body_indent,
                                           lvl + 1)

        out = 'while (' + test + ') {' + body_indent + body + closing_brace_indent + "}"
        return out

    def handle_for_range(self, gast, lvl=0):
        loop_init = router.gast_to_code(gast["init"], "java")
        loop_test = router.gast_to_code(gast["test"], "java")
        loop_update = router.gast_to_code(gast["update"], "java")

        body_indent = "\n\t" + "\t" * lvl
        closing_brace_indent = "\n" + "\t" * lvl
        body = general_helpers.list_helper(gast["body"], "java", body_indent,
                                           lvl + 1)

        return "for (" + loop_init + "; " + loop_test + "; " + loop_update + ") {" + body_indent + body + closing_brace_indent + "}"

    def handle_for_of(self, gast, lvl=0):
        arr_str = router.gast_to_code(gast["iter"], "java")
        var_name = "GenericType " + gast["init"]["value"]

        body_indent = "\n\t" + "\t" * lvl
        closing_brace_indent = "\n" + "\t" * lvl
        body = general_helpers.list_helper(gast["body"], "java", body_indent,
                                           lvl + 1)

        out = "for (" + var_name + " : " + arr_str + ") {" + body_indent + body + closing_brace_indent + "}"
        return out

    def handle_log_statement(self, gast):
        return "System.out.println"

    def handle_var_assign(self, gast):
        var_id = router.gast_to_code(gast["varId"], "java")
        var_value = router.gast_to_code(gast["varValue"], "java")

        kind = java_helpers.gast_to_java_type(gast["varValue"], error_handler=self.error_handler)

        return kind + " " + var_id + " = " + var_value

    def handle_aug_assign(self, gast):
        if "right" in gast:
            return router.gast_to_code(
                gast["left"],
                "java") + " " + gast["op"] + " " + router.gast_to_code(
                    gast["right"], "java")
        else:
            return router.gast_to_code(gast["left"], "java") + gast["op"]

    # TODO(taiga#149) gast_to_code should not be able to return System.out.println(1, 2)
    def handle_func_call(self, gast):
        # handles logstatement for single array
        if gast["value"]["type"] == "logStatement" and len(
                gast["args"]) == 1 and gast["args"][0]["type"] == "arr":
            log_statement = router.gast_to_code(gast["value"], "java")
            type_declaration = java_helpers.gast_to_java_type(gast["args"][0], error_handler=self.error_handler)
            arr = router.gast_to_code(gast["args"], "java")
            return log_statement + "(Arrays.toString(new " + type_declaration + " " + arr + "))"

        return router.gast_to_code(gast["value"],
                                   "java") + "(" + router.gast_to_code(
                                       gast["args"], "java") + ")"

    def handle_subscript(self, gast):
        pass

    def handle_name(self, gast):
        ''' 
        NOTE: some places store {"type": "name", "value": "s"} while others have
        {"type": "name", "id" : "s"} in gAST but both get routed to this func.
        We may want to re-evaluate gAST structure regarding funcs and vars
        '''
        if "value" in gast:
            return gast["value"]
        return gast["id"]

    def handle_attribute(self, gast):
        return router.gast_to_code(gast["value"], "java") + "." + gast["id"]

    def handle_built_in_attribute(self, gast):
        pass

    def handle_dict(self, gast):
        pass

    def handle_property(self, gast):
        pass

    def handle_bool_op(self, gast):
        pass

    def handle_unary_op(self, gast):
        pass

    def handle_function_declaration(self, gast, lvl=0):
        pass

    def handle_return_statement(self, gast):
        pass

    def handle_assign_pattern(self, gast):
        pass

    def handle_arr(self, gast):
        return "{" + router.gast_to_code(gast["elements"], "java") + "}"
