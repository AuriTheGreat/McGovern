import unittest

class Test_test_2(unittest.TestCase):
    def test_A(self):
        self.assertEqual(2+2, 4)

if __name__ == '__main__':
    unittest.main()
