class Number:
    def __init__(self, value) -> None:
        self.value = value

    def process(self):
        return self.value

class Variable:
    def __init__(self) -> None:
        pass

class Equation:
    def __init__(self, left, right) -> None:
        pass

class Operator:
    def __init__(self, *args):
        self.args = args


    def process(self):
        for arg in self.args:
            arg.process()
        
        self.operation()

    def operation(self):
        pass

class Addition:
    def operation(self):
        args, val = [], 0
        for arg in args:
            pass
