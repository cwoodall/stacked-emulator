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

        # INSTRUCTIONS!!! These need to be reviewed and implemented
        self.__halt     = 0x0 # EXIT/HALT
        self.__push     = 0x1 # push from memory location
        self.__pushi    = 0x2 # push an immediate value
        self.__store    = 0x3 # store TOS to memory location
        self.__dup      = 0x4 # Duplicate TOS
        self.__over     = 0x5 # Duplicate second element onto the top of the stack
        self.__swap     = 0x6 # Swap top two elements of the stack
        self.__pop      = 0x7 # POP TOS and drop it on the floor
        self.__popdr    = 0x8 # pop from data stack to return stack [FIXME: IMPLEMENT]
        self.__poprd    = 0x9 # pop from return stack to data stack [FIXME: IMPLEMENT]

        self.__bez      = 0xa # Branch If Equal to Immediate
        self.__bnez     = 0xb # Branch If Not Equal to Immediate
        self.__call     = 0xc # Put current PC ontop of return stack and jump [FIXME: IMPLEMENT]
        self.__ret      = 0xd # return [FIXME: IMPLEMENT]

        self.__alu     = 0xf # ARITHMETIC STUFF
        self.__alu_sll = 0x0 # n2 << n1 [FIXME: IMPLEMENT]
        self.__alu_sra = 0x1 # n2 >> n1 (maintain sign) [FIXME: IMPLEMENT]
        self.__alu_srl = 0x2 # n2 >> n1 (push in zeros) [FIXME: IMPLEMENT]
        self.__alu_add = 0x3 # n2 + n1 = n3 
        self.__alu_sub = 0x4 # n2 - n1 = n3 
        self.__alu_or  = 0x5 # n2 | n1 = n3 [FIXME: IMPLEMENT]
        self.__alu_and = 0x6 # n2 & n1 = n3 [FIXME: IMPLEMENT]
        self.__alu_inv = 0x7 # ~n1 = n2 [FIXME: IMPLEMENT]
        self.__alu_neg = 0x8 # -n1 = n2 [FIXME: IMPLEMENT]

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
        if opcode == self.__halt:
            print "HALT"
            self.state = 0
            self.pc -= 1
        elif opcode == self.__push:
            print "PUSHI {0}".format(self.dmem[imm])
            self.dstack.append(self.dmem[imm])
        elif opcode == self.__pushi:
            print "PUSH {0}".format(imm)
            self.dstack.append(imm)
        elif opcode == self.__store:
            self.dmem[imm] = self.dstack.pop()
            print "STORE {0}".format(self.dmem[imm])
        elif opcode == self.__dup:
            self.dstack.append(self.dstack[-1]) # duplicate the TOS
            print "DUP"
        elif opcode == self.__over:
            self.dstack.append(self.dstack[-2])
            print "OVER"
        elif opcode == self.__swap:
            n1 = self.dstack.pop()
            n2 = self.dstack.pop()
            self.dstack.append(n2)
            self.dstack.append(n1)
            print("SWAP {0} {1}".format(n1, n2))
        elif opcode == self.__bez:
            print "BZE",
            res = self.dstack.pop()
            if (res == 0):
                print "MOVE TO {0}".format(imm)
                self.pc = imm
            else:
                print "NO JUMP"
        elif opcode == self.__bnez:
            print "BNZE",
            res = self.dstack.pop()
            if (res != 0):
                print "MOVE TO {0}".format(imm)
                self.pc = imm
            else:
                print "NO JUMP"
        elif opcode == self.__alu:
            if imm == self.__alu_add:
                one = self.dstack.pop()
                two = self.dstack.pop()
                res = (two + one) & 0xFF
                print "{0} {1} ADD = {2}".format(one, two, res)
                self.dstack.append(res)
            elif imm == self.__alu_sub:
                one = self.dstack.pop()
                two = self.dstack.pop()
                res = (two - one) & 0xFF
                print "{0} {1} SUB = {2}".format(one, two, res)
                self.dstack.append(res)
def main():
    """
    Run a stacked interpreter
    """
    cpu = StackedEmulator([0x1000,0x2001, 0xf004, 0x4000, 0xb001, 0x0000], [10])
    cpu.pc_prev = -1
    while (cpu.pc != cpu.pc_prev):
        cpu.pc_prev = cpu.pc
        cpu.fetch()
        cpu.decode()
        print cpu.dstack

    return 0

if __name__ == "__main__":
    main()
