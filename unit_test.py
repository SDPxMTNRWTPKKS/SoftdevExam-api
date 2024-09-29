import unittest
from app import app  

class PrimeTestCase(unittest.TestCase):

    def test_true_when_x_is_17(self):
        response = app.show_number(17)
        self.assertEqual(response, 'True')

    def test_false_when_x_is_36(self):
        response = app.show_number(36)
        self.assertEqual(response, 'False')

    def test_true_when_x_is_13219(self):
        response = app.show_number(13219)
        self.assertEqual(response, 'True')

if __name__ == '__main__':
    unittest.main()
