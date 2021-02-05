import unittest
import Main
import requests


class MyTestCase(unittest.TestCase):
    def test_convertToArray(self):
        cases = """hi
there
me"""
        self.assertEqual(Main.convToArray(cases), ["hi", "there", "me"])

    def test_convertFromArray(self):
        case = ["hello", "world"]
        self.assertEqual(Main.convFromArray(case), """hello\nworld""")

    def test_bothConversions(self):
        cases = ["", " ", "hello", "hello\nworld", "testing\n\n1", "testing2\n\n", "\nhi\n\n2\nu\n"]
        for x in cases:
            self.assertEqual(Main.convFromArray(Main.convToArray(x)), x)

    def test_getTaskByID(self):
        foo = Main.getTaskById(0)
        self.assertEqual(str(foo),
                         """id:0, writeIDs:None, readIDsNone, public:True, title:"Hello", info:"World", linkedTasks:0""")

    def test_getUserByID(self):
        ans = "{'defaultTask': None, 'email': 'admin@example.com', 'id': 1, 'password': None, 'salt': None, 'username': 'admin'}"

        name = "admin"

        url = "http://127.0.0.1:5000/user/" + name
        response = requests.get(url)
        foo = response.json()
        # print(foo)
        # for x in foo:
        #     print(x)

        self.assertEqual(str(foo), ans)


if __name__ == '__main__':
    unittest.main()
