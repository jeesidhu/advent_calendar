import itertools
from abc import ABC, abstractmethod


class Instruction(ABC):

    @property
    @abstractmethod
    def opcode(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def execute(self, program, modes):
        pass

    @classmethod
    def create(cls, opcode):
        for subclass in cls.__subclasses__():
            if subclass.opcode == opcode:
                return subclass()
        raise Exception(f'Error: Invalid opcode: ({opcode}).')


class Add(Instruction):
    opcode = 1
    size = 4

    def execute(self, program, params):
        address = params[2].address
        value = params[0].value + params[1].value
        program.update(address, value)
        program.advance_pointer(self.size)


class Multiply(Instruction):
    opcode = 2
    size = 4

    def execute(self, program, params):
        address = params[2].address
        value = params[0].value * params[1].value
        program.update(address, value)
        program.advance_pointer(self.size)


class Halt(Instruction):
    opcode = 99
    size = 1

    def execute(self, program, modes):
        program.halt()
        program.advance_pointer(self.size)


class Input(Instruction):
    opcode = 3
    size = 2

    def execute(self, program, params):
        address = params[0].address
        value = program.get_input()
        program.update(address, value)
        program.advance_pointer(self.size)


class Output(Instruction):
    opcode = 4
    size = 2

    def execute(self, program, params):
        output = program.get(params[0].address)
        program.update_output(output)
        program.advance_pointer(self.size)


class JumpIfTrue(Instruction):
    opcode = 5
    size = 3

    def execute(self, program, params):
        if params[0].value != 0:
            address = params[1].value
            program.update_pointer(address)
        else:
            program.advance_pointer(self.size)


class JumpIfFalse(Instruction):
    opcode = 6
    size = 3

    def execute(self, program, params):
        if params[0].value == 0:
            address = params[1].value
            program.update_pointer(address)
        else:
            program.advance_pointer(self.size)


class LessThan(Instruction):
    opcode = 7
    size = 4

    def execute(self, program, params):
        address = params[2].address
        value = 1 if params[0].value < params[1].value else 0
        program.update(address, value)
        program.advance_pointer(self.size)


class Equals(Instruction):
    opcode = 8
    size = 4

    def execute(self, program, params):
        address = params[2].address
        value = 1 if params[0].value == params[1].value else 0
        program.update(address, value)
        program.advance_pointer(self.size)


class RelativeBaseOffset(Instruction):
    opcode = 9
    size = 2

    def execute(self, program, params):
        program.advance_relative_base(params[0].value)
        program.advance_pointer(self.size)


class Mode(ABC):

    @property
    @abstractmethod
    def id_(self):
        pass

    @abstractmethod
    def apply(self, program, address):
        pass

    @classmethod
    def create(cls, id_):
        for subclass in cls.__subclasses__():
            if subclass.id_ == id_:
                return subclass()
        raise Exception(f'Error: Invalid mode: ({id_}).')


class Position(Mode):
    id_ = 0

    def apply(self, program, address):
        return program.get(address)


class Immediate(Mode):
    id_ = 1

    def apply(self, program, address):
        return address


class Relative(Mode):
    id_ = 2

    def apply(self, program, address):
        return program.get(address) + program.relative_base


class Parameter:

    def __init__(self, value, address):
        self.value = value
        self.address = address

    @classmethod
    def create(cls, program, address, mode):
        address = mode.apply(program, address)
        value = program.get(address)
        return cls(value, address)


class IntCode:

    def __init__(self, values, inputs=None):
        if inputs is None:
            inputs = []
        self._memory = {k: v for k, v in enumerate(values)}
        self._extended_memory = {}
        self.pointer = 0
        self.halted = False
        self.inputs = iter(inputs)
        self.output = None
        self.relative_base = 0

    def _parse_instruction(self):
        value = str(self.get(self.pointer))
        opcode = int(value[-2:])
        modes = [Mode.create(int(i)) for i in value[:-2][::-1]]
        return opcode, modes

    def _get_parameters(self, size, modes):
        params = []
        for i in range(size - 1):
            mode = modes[i] if i < len(modes) else Position()
            address = self.pointer + i + 1
            param = Parameter.create(self, address, mode)
            params.append(param)
        return params

    def execute(self, pause_on_output=False):
        self.output = None
        while not self.halted and not (pause_on_output and self.output is not None):
            opcode, modes = self._parse_instruction()
            instruction = Instruction.create(opcode)
            parameters = self._get_parameters(instruction.size, modes)
            instruction.execute(self, parameters)
        return self.output

    def get(self, address):
        return self._memory[address] \
            if address < len(self._memory) \
            else self._extended_memory.get(address, 0)

    def update(self, address, value):
        if address < len(self._memory):
            self._memory[address] = value
        else:
            self._extended_memory[address] = value

    def update_pointer(self, address):
        self.pointer = address

    def advance_pointer(self, amount):
        self.pointer += amount

    def halt(self):
        self.halted = True

    def update_output(self, value):
        self.output = value

    def advance_relative_base(self, amount):
        self.relative_base += amount

    def get_input(self):
        try:
            value = next(self.inputs)
        except StopIteration:
            raise Exception(f'Error: No input value provided.')
        except:
            raise
        return value

    def add_to_inputs(self, value):
        self.inputs = itertools.chain(self.inputs, [value])
