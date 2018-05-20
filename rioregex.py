from utils import clearAndReplaceList


# simple enum(s) for special state(s)
STATE_MATCH = 1

METACHARS = set(['.', '?',
                '*', '+'])


class RegexEngine:

    def __init__(self):
        pass

    def match(self, pattern, text):
        # Matches pattern with String.
        # boilerplate parse, compile machine, then run/walk said machine.
        pass

    @staticmethod
    def _compile(regexp):
        # convert regexp string into a state machine. Returns state entry obj.

        if not regexp:
            return

        # todo: determine and raise exception if reg ends with meta
        # todo: determine and raise exception if certain metas are proceeded by other certain metas
        # todo: what if it starts with a meta? refactor
        firstState = State(regexp[0])
        prevStateCache = [firstState]  # keep running record of dangling states prev loop made

        # todo: DRY what can be DRYed
        regexChars = iter(regexp[1:])
        for char in regexChars:
            if char not in METACHARS:
                newState = State(char)
                # stitch together previous dangling states
                for prev in prevStateCache:
                    prev.nextState = newState
                clearAndReplaceList(prevStateCache, [newState])

            elif char == '*':
                # state goes to any char, or repeats self if same char.
                char = next(regexChars)  # get the character one ahead of me.
                newState = State(char)
                # the loop back
                newState.nextStateAlt = newState
                for prev in prevStateCache:
                    prev.nextState = newState
                clearAndReplaceList(prevStateCache, [newState])

            elif char == '?':
                # 0 or 1 match. So 1 one arrow goes to another copy of target char, other to char after it.
                char = next(regexChars)
                newState = State(char)
                oneState = State(char)
                # arrow to identical-by-value State ('1' case)
                newState.nextStateAlt = oneState
                # '0 state' is whatever next char stiches to nextState.
                for prev in prevStateCache:
                    prev.nextState = newState
                # two dangling states to stitch with next round
                clearAndReplaceList(prevStateCache, [newState, oneState])

            elif char == '.':
                # matches anything. Can be treated like literal. 'any' logic would occur in SM walker
                newState = State(char)
                for prev in prevStateCache:
                    prev.nextState = newState
                clearAndReplaceList(prevStateCache, [newState])

            elif char == '+':
                # 1 or many times.
                char = next(regexChars)
                # 'hardwire' one step in the machine
                oneState = State(char)
                oneState.nextState = newState(char) # equiv to * state.
                newState.nextStateAlt = newState
                for prev in prevStateCache:
                    prev.nextState = oneState
                clearAndReplaceList(prevStateCache, [newState])

        # and at last tie it all up.
        for prev in prevStateCache:
            prev.nextState = STATE_MATCH

        return firstState


class State:

    def __init__(self, char):
        self.char = char
        # two possible out states. nextState must always be set at the end
        # of SM construction
        self.nextState = None
        self.nextStateAlt = None

    def __repr__(self):
        return 'State {char} {id}'.format(char=self.char,
                                          id=id(self))

    def advanceToNextState(self, inputChar):
        # transition to next state based on input and outstate values.
        # todo: or, sublcass state and designate this a virtual func,
        # with logic done in subclasses
        pass


if __name__ == "__main__":
    print("cmdline funcs to come")
