from opcodes import *

class StackFullError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

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

    Instructions are 16-bits wide, all data paths are 16 bits.
    """
    def __init__(self, pmem, dmem, N=32): # Initialize pmem and dmem
        self.pmem = pmem # program memory 
        self.dmem = dmem # data memory [FIXME]
        self.pc = 0      # Program Counter
        self.dstack = [] # data stack of size N
        self.rstack = [] # return stack
        self.ir = 0      # current instruction register
        self.N = N

    def fetch(self):
        """
        Load instruction from program memory into the instruction register.
        """
        self.ir = self.pmem[self.pc]

    def __popr(self):
        return self.rstack.pop()

    def __popd(self):
        return self.dstack.pop()

    def __pushr(self, val):
        if len(self.rstack) < self.N:
            self.rstack.append(val)
            return 0
        else:
            raise

    def __pushd(self, val):
        if len(self.dstack) < self.N:
            self.dstack.append(val)
            return 0
        else:
            raise

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
            try:
                self.__pushd(self.dmem[imm])
            except:
                print "Oh No... Stack Full"
        elif opcode == Opcodes.PUSHI:
            print "PUSH {0}".format(imm)
            try:
                self.__pushd(imm)
            except:
                print "Oh No... Stack Full"
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