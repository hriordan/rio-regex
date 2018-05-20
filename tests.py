import unittest
from rioregex import RegexEngine, STATE_MATCH


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


class TestStateMachine(unittest.TestCase):

    def test_compileBasicRegexToStateMachine(self):
        # just a basic phrase w/ no metachars
        regex = "abc"
        state = RegexEngine._compile(regex)
        self.assertNotEqual(state, None)
        for char in regex:
            self.assertEqual(state.char, char)
            self.assertEqual(state.nextStateAlt, None)
            state = state.nextState

        self.assertEqual(state, STATE_MATCH)

    def test_compileEmptyexpr(self):
        regex = ''
        state = RegexEngine._compile(regex)
        self.assertEqual(state, None)

    def test_compileStarExpr(self):
        regex = "a*bc"
        start = RegexEngine._compile(regex)
        state = start

        self.assertEqual(state.char, 'a')
        self.assertNotEqual(state.nextState, None)
        self.assertEqual(state.nextStateAlt, None)

        state = state.nextState

        self.assertEqual(state.char, 'b')
        self.assertNotEqual(state.nextState, None)
        self.assertEqual(state.nextStateAlt, state)

        state = state.nextState
        self.assertEqual(state.char, 'c')
        self.assertEqual(state.nextState, STATE_MATCH)
        self.assertEqual(state.nextStateAlt, None)

    def test_compileQuesMarkExpr(self):
        # string with a ? in it
        pass

    def test_compileDotExpr(self):
        # string with a . in it
        pass

    def test_compilePlusExpr(self):
        # expr with a + in it
        pass

    def test_compileComplexExpr(self):
        # try various exprs with a combination of all metachars.
        # The final boss of tests if you will; how many combos should I try?
        pass

    # todo: Implement and test transition functions ('advanceToNext')


if __name__ == '__main__':
    unittest.main()
