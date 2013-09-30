from opcodes import *

class Assembler(object):
    """
    Assembles a program into machine code
    """

    def __init__(self, prog):
        if isinstance(prog, str):
            prog = prog.split("\n")
        self.prog = [i.strip() for i in prog if len(i.strip()) > 0]
        self.code = []

    
    def assemble(self):
        #if len(self.code) > 0:
        for instr in self.prog:
            self.code.append(self.__encode(instr))
        return self.code


    def __encode(self, instr):
        parts = instr.split(" ")
        op = parts[0].strip()
        arg = parts[1].strip() if len(parts) > 1 else None

        try:
            opcode = Opcodes.__dict__[op.upper()]
            imm = eval(arg) if arg else 0
            alu = False
        except KeyError:
            opcode = Opcodes.__dict__["ALU_%s"%op.upper()]
            alu = True

        if alu:
            enc = 0xf000 | opcode
        else:
            enc = opcode << 12 | imm

        return enc
