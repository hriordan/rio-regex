import unittest
from rioregex import RegexEngine


class TestRegex(unittest.TestCase):

    def setUp(self):
        self.re = RegexEngine()

    def test_basicMatch(self):
        # exact match
        self.assertTrue(self.re.match("abc", "abc"))
        # mismatch by any character
        self.assertFalse(self.re.match("abd", "abc"))

    def test_anyCharacterMatch(self):
        self.assertTrue(self.re.match("a.c", "abc"))

    def test_optionalCharMatch(self):
        self.assertTrue(self.re.match("a?bc", "abc"))
        self.assertTrue(self.re.match("a?bc", "ac"))
        # can match, but doesnt have to. TODO move to own test?
        self.assertTrue(self.re.match("?aab", "ab"))


# todo: test state machine funcs

class TestStateMachine(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
