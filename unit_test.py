import unittest
from app import app  

class PrimeTestCase(unittest.TestCase):

    def test_true_when_x_is_1(self):
        response = app.show_number(1)
        self.assertEqual(response, 'True')

    def test_false_when_x_is_0(self):
        response = app.show_number(0)
        self.assertEqual(response, 'False')

    def test_true_when_x_is_nev2(self):
        response = app.show_number(-2)
        self.assertEqual(response, 'False')

if __name__ == '__main__':
    unittest.main()
