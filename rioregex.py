
# simple enum(s) for special states
STATE_MATCH = 1


# TODO: A skeleton, will be filled out
class RegexEngine:

    def __init__(self):
        pass

    def match(self, pattern, text):
        #  Matches pattern with String.
        # boilerplate parse, compile machine, then run
        pass

    def _compile(self, regex):
        # convert into a State object, repping the state machine
        pass


class State:
    def __init__(self, char):
        self.char = char
        # todo: better names
        # two possible out states. nextState must always be set at the end
        self.nextState = None
        # can be set (for + or *), or be none
        self.nextStateAlt = None

    def __repr__(self):
        return 'State {char}'.format(char=self.char)

    def evaluateInput(self, inputChar):
        pass


# todo: this is prototype function, move inside _compile() method
def buildStateMachine(regexp):
    if not regexp:
        return

    # build the first guy
    firstState = State(regexp[0])
    prevState = firstState

    for char in regexp[1:]:
        newState = State(char)
        # todo: fashion cases for metachars
        if prevState:
            prevState.nextState = newState
        prevState = newState

    # and at last.
    prevState.nextState = STATE_MATCH

    return firstState


# TODO: move to more suitable place for helper/debug funcs
def printStateMachine(state):
    if not state:
        print("got nothing")
        return
    while state and state.nextState != STATE_MATCH:
        print("State {}, outs ({}, {})".format(
              state, state.nextState, state.nextStateAlt))
        state = state.nextState
    print("reached state match!")


if __name__ == "__main__":
    print("cmdline funcs to come")
