import unittest2
import translate
import test_matrix


class TestLoops(unittest2.TestCase):

    def test_while_simple(self):
        js_code = 'while (true) {\n\t5\n}'
        py_code = 'while (True):\n\t5'
        java_code = 'while (true) {\n\t5;\n}'
        test_matrix.test(self, py_code, js_code, java_code)

    def test_while_range(self):
        js_code = 'while (x < 10) {\n\t5\n}'
        py_code = 'while (x < 10):\n\t5'
        java_code = 'while (x < 10) {\n\t5;\n}'
        test_matrix.test(self, py_code, js_code, java_code)

    def test_for_range_increment_one(self):
        js_code = 'for (let i = 0; i < 10; i += 1) {\n\t5\n}'
        py_code = 'for i in range (0, 10, 1):\n\t5'
        java_code = 'for (int i = 0; i < 10; i += 1) {\n\t5;\n}'
        test_matrix.test(self, py_code, js_code, java_code)

    def test_for_range_implied_increment_one(self):
        """
        When python's step argument is ommitted, step=1. This test checks
        to make sure functionality is maintained when arg is ommitted.
        """
        input_py_code = 'for i in range (0, 10):\n\t5'
        expected_js_code = 'for (let i = 0; i < 10; i += 1) {\n\t5\n}'
        expected_java_code = 'for (int i = 0; i < 10; i += 1) {\n\t5;\n}'
        self.assertEqual(expected_js_code,
                         translate.translate(input_py_code, 'py', 'js'))
        self.assertEqual(expected_java_code,
                         translate.translate(input_py_code, 'py', 'java'))

    def test_for_range_increment_two(self):
        js_code = 'for (let i = 0; i < 10; i += 2) {\n\t5\n}'
        py_code = 'for i in range (0, 10, 2):\n\t5'
        java_code = 'for (int i = 0; i < 10; i += 2) {\n\t5;\n}'
        test_matrix.test(self, py_code, js_code, java_code)

    def test_for_inclusiverange_increment_two(self):
        """
        Since python does not have inclusive range, it needs to adjust the end point
        of the range to be effectively inclusive. This test confirms this functionality
        """
        input_js_code = 'for (let i = 0; i <= 10; i += 2) {\n\t5\n}'
        expected_py_code = 'for i in range (0, 12, 2):\n\t5'
        self.assertEqual(expected_py_code,
                         translate.translate(input_js_code, 'js', 'py'))

    def test_for_with_update_expression_plus(self):
        input_js_code = 'for (let i = 0; i <= 10; i++) {\n\t5\n}'
        input_java_code = 'for (int i = 0; i <= 10; i++) {\n\t5;\n}'
        expected_py_code = 'for i in range (0, 11, 1):\n\t5'
        self.assertEqual(expected_py_code,
                         translate.translate(input_js_code, 'js', 'py'))
        self.assertEqual(expected_py_code,
                         translate.translate(input_java_code, 'java', 'py'))

    def test_for_with_update_expression_minus(self):
        input_js_code = 'for (let i = 20; i >= -5; i--) {\n\t5\n}'
        input_java_code = 'for (int i = 20; i >= -5; i--) {\n\t5;\n}'
        expected_py_code = 'for i in range (20, -4, -1):\n\t5'
        self.assertEqual(expected_py_code,
                         translate.translate(input_js_code, 'js', 'py'))
        self.assertEqual(expected_py_code,
                         translate.translate(input_java_code, 'java', 'py'))

    def test_for_loop_python_incrementor(self):
        input_py_code = 'for i in range(0,10,1): \n\t5'
        expected_js_code = 'for (let i = 0; i < 10; i += 1) {\n\t5\n}'
        expected_java_code = 'for (int i = 0; i < 10; i += 1) {\n\t5;\n}'
        self.assertEqual(expected_js_code,
                         translate.translate(input_py_code, 'py', 'js'))
        self.assertEqual(expected_java_code,
                         translate.translate(input_py_code, 'py', 'java'))

    def test_for_range_increment_negative(self):
        js_code = 'for (let i = 10; i > 0; i -= 1) {\n\t5\n}'
        py_code = 'for i in range (10, 0, -1):\n\t5'
        java_code = 'for (int i = 10; i > 0; i -= 1) {\n\t5;\n}'
        test_matrix.test(self, py_code, js_code, java_code)

    def test_for_range_all_args_neg(self):
        js_code = 'for (let i = -25; i > -50; i -= 5) {\n\t5\n}'
        py_code = 'for i in range (-25, -50, -5):\n\t5'
        test_matrix.test(self, py_code, js_code)

    def test_for_range_one_arg_loop(self):
        ''' 
        users can give range 1 args - translations give range 3 args 
        hence js -> py is not supported for this translation 
        '''
        js_code = 'for (let i = 0; i < 5; i += 1) {\n\tconsole.log(i)\n}'
        py_code = 'for i in range (5):\n\tprint(i)'
        self.assertEqual(js_code, translate.translate(py_code, 'py', 'js'))

    def test_forOf(self):
        js_code = 'for (elem of [1, 2]) {\n\t5\n}'
        py_code = 'for elem in [1, 2]:\n\t5'
        self.assertEqual(py_code, translate.translate(js_code, "js", "py"))
        self.assertEqual(js_code, translate.translate(py_code, "py", "js"))

    def test_forOf_with_java(self):
        js_code = 'for (elem of arr) {\n\t5\n}'
        py_code = 'for elem in arr:\n\t5'
        java_code = 'for (GenericType elem : arr) {\n\t5;\n}'
        test_matrix.test(self, py_code, js_code, java_code)


if __name__ == '__main__':
    unittest2.main()
