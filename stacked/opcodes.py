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
