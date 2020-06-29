import unittest2
import sys

sys.path.append('translate')
sys.path.append('translate/assign')
sys.path.append('translate/expression')
sys.path.append('translate/conditional')
sys.path.append('translate/helpers')
sys.path.append('translate/routers')

import py_main


class test_py_to_gast_conditionals(unittest2.TestCase):
    def test_ifs(self):
        py_code = 'if (True):\n\tprint("This is true")'   
        expected_gast = {
            'type': 'root',
            'body': [{
                'type': 'if',
                 'body': [{
                     'type': 'logStatement',
                     'args': [{'type': 'str', 'value': 'This is true'}]
                    }],
                'orelse': [],
                'test': {'type': 'bool', 'value': 1}
                }]
            }
        self.assertEqual(expected_gast, py_main.py_to_gast(py_code))

    def test_else(self):
        py_code = 'if (1):\n\tprint("1 is true")\nelse:\n\tprint("1 is NOT true")\n'
        expected_gast = {
            'type': 'root', 
            'body': [{
                'type': 'if',
                'body': [{
                     'type': 'logStatement', 
                     'args': [{'type': 'str', 'value': '1 is true'}]
                     }], 
                'orelse': [{
                         'type': 'logStatement',
                         'args': [{'type': 'str', 'value': '1 is NOT true'}]
                         }], 
                'test': {'type': 'num', 'value': 1}
                }]
            }
        self.assertEqual(expected_gast, py_main.py_to_gast(py_code))
   
    def test_elif(self):
        py_code = 'if (1):\n\tprint("1 is true")\nelif (2):\n\tprint("2 is true")\n\tprint("second line")\n'
        expected_gast = {
            'type': 'root', 
            'body': [{
                'type': 'if', 
                'body': [{
                    'type': 'logStatement', 
                    'args': [{'type': 'str', 'value': '1 is true'}]
                    }], 
                'orelse': [{
                    'type': 'if', 
                    'body': [
                        {
                        'type': 'logStatement', 
                        'args': [{'type': 'str', 'value': '2 is true'}]
                        },
                        {
                        'type': 'logStatement', 
                        'args': [{'type': 'str', 'value': 'second line'}]
                        }
                    ], 
                    'orelse': [], 
                    'test': {'type': 'num', 'value': 2}
                    }], 
                'test': {'type': 'num', 'value': 1}
                }]
            }     
        self.assertEqual(expected_gast, py_main.py_to_gast(py_code))

if __name__ == '__main__':
    unittest2.main()