import unittest2
import python.code_to_gast.py_main as py_main
import javascript.code_to_gast.js_main as js_main
import java.code_to_gast.java_main as java_main
from test.error_handler_helper import get_error_handler


class test_code_to_gast_conditionals(unittest2.TestCase):
    maxDiff = None

    def test_ifs(self):
        py_code = 'if (True):\n\tprint("This is true")'
        js_code = 'if (true) {\n\tconsole.log("This is true")\n}'
        java_code = 'if (true) {System.out.println("This is true");}'
        expected_gast = {
            'type':
                'root',
            'body': [{
                'type': 'if',
                'body': [{
                    'type': 'funcCall',
                    'value': {
                        'type': 'logStatement'
                    },
                    'args': [{
                        'type': 'str',
                        'value': 'This is true'
                    }]
                }],
                'orelse': [],
                'test': {
                    'type': 'bool',
                    'value': 1
                }
            }]
        }
        self.assertEqual(
            expected_gast,
            py_main.py_to_gast(py_code))
        self.assertEqual(
            expected_gast,
            js_main.js_to_gast(js_code))
        self.assertEqual(
            expected_gast,
            java_main.java_to_gast(java_code))

    def test_else(self):
        py_code = 'if (1):\n\tprint("1 is true")\nelse:\n\tprint("1 is NOT true")\n'
        js_code = 'if (1) {\n\tconsole.log("1 is true")\n} else {\n\tconsole.log("1 is NOT true")\n}'  # TODO: consider adding ; after console.log()
        java_code = 'if (1) {System.out.println("1 is true");} else {System.out.println("1 is NOT true");}'
        expected_gast = {
            'type':
                'root',
            'body': [{
                'type': 'if',
                'body': [{
                    'type': 'funcCall',
                    'value': {
                        'type': 'logStatement'
                    },
                    'args': [{
                        'type': 'str',
                        'value': '1 is true'
                    }]
                }],
                'orelse': [{
                    'type': 'funcCall',
                    'value': {
                        'type': 'logStatement'
                    },
                    'args': [{
                        'type': 'str',
                        'value': '1 is NOT true'
                    }]
                }],
                'test': {
                    'type': 'num',
                    'value': 1
                }
            }]
        }
        self.assertEqual(
            expected_gast,
            py_main.py_to_gast(py_code))
        self.assertEqual(
            expected_gast,
            js_main.js_to_gast(js_code))
        self.assertEqual(
            expected_gast,
            java_main.java_to_gast(java_code))

    def test_elif(self):
        py_code = 'if (1):\n\tprint("1 is true")\nelif (2):\n\tprint("2 is true")\n\tprint("second line")\n'
        js_code = 'if (1) {\n\tconsole.log("1 is true")\n} else if (2) {\n\tconsole.log("2 is true")\n\tconsole.log("second line")\n}'
        java_code = 'if (1) {System.out.println("1 is true");} else if (2) {System.out.println("2 is true"); System.out.println("second line");}'
        expected_gast = {
            'type':
                'root',
            'body': [{
                'type': 'if',
                'body': [{
                    'type': 'funcCall',
                    'value': {
                        'type': 'logStatement'
                    },
                    'args': [{
                        'type': 'str',
                        'value': '1 is true'
                    }]
                }],
                'orelse': [{
                    'type': 'if',
                    'body': [{
                        'type': 'funcCall',
                        'value': {
                            'type': 'logStatement'
                        },
                        'args': [{
                            'type': 'str',
                            'value': '2 is true'
                        }]
                    }, {
                        'type': 'funcCall',
                        'value': {
                            'type': 'logStatement'
                        },
                        'args': [{
                            'type': 'str',
                            'value': 'second line'
                        }]
                    }],
                    'orelse': [],
                    'test': {
                        'type': 'num',
                        'value': 2
                    }
                }],
                'test': {
                    'type': 'num',
                    'value': 1
                }
            }]
        }
        self.assertEqual(
            expected_gast,
            py_main.py_to_gast(py_code))
        self.assertEqual(
            expected_gast,
            js_main.js_to_gast(js_code))
        self.assertEqual(
            expected_gast,
            java_main.java_to_gast(java_code))


if __name__ == '__main__':
    unittest2.main()
