from utils import clearAndReplaceList, STATE_MATCH, METACHARS, printStateMachine
from state import (StateLiteral, StateStar,
                   StateQuesMark, StateDot,
                   StateError)


class RegexEngine:

    def __init__(self):
        pass

    # TODO: convert to DFA, NFA gets scared on branching

    def match(self, regexp, text):
        # Matches pattern with String.
        # boilerplate parse, compile machine, then run/walk said machine.
        #TODO: check regex string for illegal patterns

        state = self._compile(regexp)
        # printStateMachine(state)
        for char in text:
            try:
                state = state.decideNextState(char)
            except StateError as e:
                # todo: print/log where it couldnt proceed
                print("state machine %s w text %s couldntrun" % (regexp, text))
                return False
            except ValueError:  # TODO: or something more precise
                print("string too long or short tbd")
                return False

        return True

    @staticmethod
    def _compile(regexp):
        # convert regexp string into a state machine. Returns state entry obj.

        if not regexp:
            return

        # todo: determine and raise exception if reg ends with bad metas
        # todo: determine and raise exception if certain metas are proceeded by other certain metas

        prevStateCache = []  # keep running record of dangling states prev loop made

        # todo: DRY what can be DRYed
        regexChars = iter(regexp)
        firstState = None

        for char in regexChars:
            if char not in METACHARS:
                newState = StateLiteral(char)
                # stitch together previous dangling states
                for prev in prevStateCache:
                    prev.nextState = newState
                clearAndReplaceList(prevStateCache, [newState])

            elif char == '*':
                # state goes to any char, or repeats self if same char.
                char = next(regexChars)  # get the character one ahead of me.
                newState = StateStar(char)
                # the loop back
                newState.nextStateAlt = newState
                for prev in prevStateCache:
                    prev.nextState = newState
                clearAndReplaceList(prevStateCache, [newState])

            elif char == '?':
                # 0 or 1. So 1 one arrow goes to another copy of target char, other to char after it.
                char = next(regexChars)
                newState = StateQuesMark(char)
                oneState = StateLiteral(char)  # identical state
                newState.nextStateAlt = oneState

                # '0 state' is whatever next char stiches to nextState.
                for prev in prevStateCache:
                    prev.nextState = newState
                # two dangling states to stitch with next round
                clearAndReplaceList(prevStateCache, [newState, oneState])

            elif char == '.':
                # matches anything. Can be treated like literal. 'any' logic would occur in SM walker
                newState = StateDot(char)
                for prev in prevStateCache:
                    prev.nextState = newState
                clearAndReplaceList(prevStateCache, [newState])

            elif char == '+':
                # 1 or many times.
                char = next(regexChars)
                # 'hardwire' one step in the machine
                oneState = StateLiteral(char)
                newState = StateStar(char)

                oneState.nextState = newState
                newState.nextStateAlt = newState

                for prev in prevStateCache:
                    prev.nextState = oneState
                clearAndReplaceList(prevStateCache, [newState])

            if not firstState:
                firstState = newState

        # tie up the last state transitions
        for prev in prevStateCache:
            prev.nextState = STATE_MATCH

        return firstState


if __name__ == "__main__":
    print("cmdline funcs to come")
