import unittest

class Test_test_1(unittest.TestCase):
    def test_A(self):
        self.assertEqual(2+2, 4)

if __name__ == '__main__':
    unittest.main()
