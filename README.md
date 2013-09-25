# Stacked Emulator: An Emulator for Stacked, A Stack Machine

This is an emulator for the begining stages of Stacked, which is a 16-bit stack machine ISA.
The current goal is to come up with an ISA for a stack machine and document what I learn
about computer architecture and stack machines! The end goal is to produce a small FPGA 
implementation of Stacked with a focus on acting as a network interface for UARTS,
I2C, end Ethernet (as a TCP/IP stack).

Previously created stack machines (for FPGA), both of which have similar goals:
- uCore: http://www.microcore.org/
- J1: http://www.excamera.com/files/j1.pdf

I am very likely to pull heavily from J1 and uCore as well as older stack machine architectures.
I don't plan on being super innovative, but I also am not aiming to maintain cross compatibility.

Some interesting stuff from a CMU course book: http://www.ece.cmu.edu/~koopman/stack_computers/sec3_2.html

The stacked emulator is currently written in Python. There is some thought of 
moving the emulator over to javascript so it can live online like
the [sx86-emulator](https://github.com/cwoodall/sx86-emulator) and provide
a similar interface for using it and debugging. That said, I much prefer python.
