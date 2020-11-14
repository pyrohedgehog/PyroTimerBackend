import unittest
import Main

class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)

    def test_convToArray(self):
        cases = """hi
there
me"""
        self.assertEqual(Main.convToArray(cases), ["hi", "there", "me"])

    def test_convFromArray(self):
        case = ["hello", "world"]
        self.assertEqual(Main.convFromArray(case), """hello\nworld""")

    def test_bothConv(self):
        cases = ["", " ", "hello", "hello\nworld", "testing\n\n1", "testing2\n\n","\nhi\n\n2\nu\n"]
        for x in cases:
            self.assertEqual(Main.convFromArray(Main.convToArray(x)), x)

print(Main.genSalt())
if __name__ == '__main__':
    unittest.main()

