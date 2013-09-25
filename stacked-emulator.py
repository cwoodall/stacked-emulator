
class Opcodes(object):
    """
    The varios instructions the CPU understands

    Pulled into own class so other things (assembler, etc) can reference
    """
    # INSTRUCTIONS!!! These need to be reviewed and implemented
    HALT     = 0x0 # EXIT/HALT
    PUSH     = 0x1 # push from memory location
    PUSHI    = 0x2 # push an immediate value
    STORE    = 0x3 # store TOS to memory location
    DUP      = 0x4 # Duplicate TOS
    OVER     = 0x5 # Duplicate second element onto the top of the stack
    SWAP     = 0x6 # Swap top two elements of the stack
    POP      = 0x7 # POP TOS and drop it on the floor
    POPDR    = 0x8 # pop from data stack to return stack [FIXME: IMPLEMENT]
    POPRD    = 0x9 # pop from return stack to data stack [FIXME: IMPLEMENT]

    BEZ      = 0xa # Branch If Equal to Immediate
    BNEZ     = 0xb # Branch If Not Equal to Immediate
    CALL     = 0xc # Put current PC ontop of return stack and jump [FIXME: IMPLEMENT]
    RET      = 0xd # return [FIXME: IMPLEMENT]

    ALU      = 0xf # ARITHMETIC STUFF
    ALU_SLL  = 0x0 # n2 << n1 [FIXME: IMPLEMENT]
    ALU_SRA  = 0x1 # n2 >> n1 (maintain sign) [FIXME: IMPLEMENT]
    ALU_SRL  = 0x2 # n2 >> n1 (push in zeros) [FIXME: IMPLEMENT]
    ALU_ADD  = 0x3 # n2 + n1 = n3 
    ALU_SUB  = 0x4 # n2 - n1 = n3 
    ALU_OR   = 0x5 # n2 | n1 = n3 [FIXME: IMPLEMENT]
    ALU_AND  = 0x6 # n2 & n1 = n3 [FIXME: IMPLEMENT]
    ALU_INV  = 0x7 # ~n1 = n2 [FIXME: IMPLEMENT]
    ALU_NEG  = 0x8 # -n1 = n2 [FIXME: IMPLEMENT]


class StackedEmulator(object):
    """
    Stacked is a basic stack machine emulator. The memory architecture and structure
    follows a Harvard Architecture:

    +-----------+       +-------------+
    | CPU       |<=====>| Data Memory |
    |           |       +-------------+
    |           |
    |           |       +----------------+
    |           |<=====>| Program Memory |
    |           |       +----------------+
    +-----------+

    Instructions are 16-bits wide, all data paths are 16 bits. (FIXME bad move?)
    """
    def __init__(self, pmem, dmem): # Initialize pmem and dmem
        self.pmem = pmem # program memory 
        self.dmem = dmem # data memory [FIXME]
        self.pc = 0      # Program Counter
        self.dstack = [] # data stack
        self.rstack = [] # return stack
        self.ir = 0      # current instruction register


    def fetch(self):
        """
        Load instruction from program memory into the instruction register.
        """
        self.ir = self.pmem[self.pc]

    def decode(self, cmd=None):
        """
        Decode things
        """
        opcode = (self.ir & 0xf000) >> 12
        imm = (self.ir & 0x0fff)
        state = 1
        self.pc += 1
        if opcode == Opcodes.HALT:
            print "HALT"
            self.state = 0
            self.pc -= 1
        elif opcode == Opcodes.PUSH:
            print "PUSHI {0}".format(self.dmem[imm])
            self.dstack.append(self.dmem[imm])
        elif opcode == Opcodes.PUSHI:
            print "PUSH {0}".format(imm)
            self.dstack.append(imm)
        elif opcode == Opcodes.STORE:
            self.dmem[imm] = self.dstack.pop()
            print "STORE {0}".format(self.dmem[imm])
        elif opcode == Opcodes.DUP:
            self.dstack.append(self.dstack[-1]) # duplicate the TOS
            print "DUP"
        elif opcode == Opcodes.OVER:
            self.dstack.append(self.dstack[-2])
            print "OVER"
        elif opcode == Opcodes.SWAP:
            n1 = self.dstack.pop()
            n2 = self.dstack.pop()
            self.dstack.append(n2)
            self.dstack.append(n1)
            print("SWAP {0} {1}".format(n1, n2))
        elif opcode == Opcodes.BEZ:
            print "BZE",
            res = self.dstack.pop()
            if (res == 0):
                print "MOVE TO {0}".format(imm)
                self.pc = imm
            else:
                print "NO JUMP"
        elif opcode == Opcodes.BNEZ:
            print "BNZE",
            res = self.dstack.pop()
            if (res != 0):
                print "MOVE TO {0}".format(imm)
                self.pc = imm
            else:
                print "NO JUMP"
        elif opcode == Opcodes.ALU:
            if imm == Opcodes.ALU_ADD:
                one = self.dstack.pop()
                two = self.dstack.pop()
                res = (two + one) & 0xFF
                print "{0} {1} ADD = {2}".format(one, two, res)
                self.dstack.append(res)
            elif imm == Opcodes.ALU_SUB:
                one = self.dstack.pop()
                two = self.dstack.pop()
                res = (two - one) & 0xFF
                print "{0} {1} SUB = {2}".format(one, two, res)
                self.dstack.append(res)


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


def main():
    """
    Run a stacked interpreter
    """

    code = """
    push 0    
    pushi 1
    sub
    dup
    bnez 1
    halt
    """

    asm = Assembler(code)
    code = asm.assemble()
    cpu = StackedEmulator(code, [10])
    cpu.pc_prev = -1
    while (cpu.pc != cpu.pc_prev):
        cpu.pc_prev = cpu.pc
        cpu.fetch()
        cpu.decode()
        print cpu.dstack

    return 0

if __name__ == "__main__":
    main()

