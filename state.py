class State:

    def __init__(self, char):
        self.char = char
        # two possible out states. nextState must always be set at the end
        self.nextState = None
        self.nextStateAlt = None

    def __repr__(self):
        return '{klass} {char} {id}'.format(klass=self.__class__,
                                            char=self.char,
                                            id=id(self))

    def decideNextState(self, inputChar):
        #  this a virtual func, with logic done in subclasses
        pass


class StateError(BaseException):
    """should raise when state cannot transition"""
    pass


class StateLiteral(State):

    def decideNextState(self, inputChar):
        if self.char == inputChar:
            return self.nextState
        raise StateError("state cannot move to next")


class StateStar(State):

    def decideNextState(self, inputChar):
        # if the next two states take the same char, choose the next literal
        if self.nextState.char == self.nextStateAlt.char:
            return self.nextState.decideNextState(inputChar)

        if self.char == inputChar:
            return self.nextStateAlt  # this should me!

        # otherwise next state should be the evaluator.
        return self.nextState.decideNextState(inputChar)


class StateQuesMark(State):

    def decideNextState(self, inputChar):
        # god damn it has to try  both

        if self.char != inputChar:
            # the 0 case.
            return self.nextState.decideNextState(inputChar)
        # char literal
        return self.nextStateAlt.decideNextState(inputChar)


# needed? equiv to a literal and a star
class StatePlus(State):
    def decideNextState(self, inputChar):
        pass


class StateDot(State):

    def decideNextState(self, inputChar):
        return self.nextState
