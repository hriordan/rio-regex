
# simple enum(s) for special state(s)
STATE_MATCH = 1

METACHARS = set(['.', '?',
                '*', '+'])


def clearAndReplaceList(old, new):
    old.clear()
    old.extend(new)


# useful for debugging
def printStateMachine(state):
    if not state:
        print("got nothing")
        return
    while state and state != STATE_MATCH:
        print("{},\n   outs ({}, {})".format(
              state, state.nextState, state.nextStateAlt))
        state = state.nextState
    print("reached state match")
