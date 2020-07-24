from flask import abort
import javascript.code_to_gast.js_main as js_main
import python.code_to_gast.py_main as py_main
import java.code_to_gast.java_main as java_main
import shared.gast_to_code.gast_to_code_router as gtc
import shared.gast_to_code.general_helpers as general_helpers
from data_service import DataService
import subprocess
from shared.gast_to_code.converter_registry import ConverterRegistry

"""
input_code: string representing input code
input_lang: string representing input language of code
output_lang: string representing output language of code
return: string representing output code or error message
"""


def translate(input_code, input_lang, output_lang):
    error_handler = ConverterRegistry.get_converter(output_lang).get_error_handler()

    # code to gast
    gast = code_to_gast_caller(input_code, input_lang, error_handler)
    if (not is_valid_gast(gast)):
        output_code = error_handler.compilation()
        return output_code

    #gast to code
    output_code = gast_to_code_caller(gast, output_lang, error_handler)

    # analytics
    store_analytics_caller(input_code, output_code, input_lang, output_lang)

    return output_code


def code_to_gast_caller(input_code, input_lang, error_handler):
    # TODO(taiga#172): remove hard coded references
    if input_lang == "js":
        gast = js_main.js_to_gast(input_code, error_handler)
    elif input_lang == "py":
        gast = py_main.py_to_gast(input_code, error_handler)
    elif input_lang == "java":
        gast = java_main.java_to_gast(input_code, error_handler)
    else:
        # TODO: use error handler
        return "Error must specify input language. For example, js for javascript and py for python"

    return gast





def is_valid_gast(gast):
    if (type(gast) == dict):
        return True
    else:
        return False


def gast_to_code_caller(gast, output_lang, error_handler):
    try:
        output_code = gtc.gast_to_code(gast, output_lang)

        if output_lang == "java":
            output_code = general_helpers.java_linter(output_code)

        return output_code
    except:
        return "Error: unable to convert generic ast to code"


def store_analytics_caller(input_code, output_code, input_lang, output_lang):
    # if the user deletes their translation don't store empty translation "" -> ""
    if (input_code == "" and output_code == ""):
        pass
    else:
        # store translation on firebase
        data_service = DataService.getInstance()
        data_service.store_query(input_code, output_code, input_lang,
                                 output_lang)
