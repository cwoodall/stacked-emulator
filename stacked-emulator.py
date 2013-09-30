from stacked import *

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

