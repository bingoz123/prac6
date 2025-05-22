#!/usr/bin/env python3
# VMTranslator.py

import sys

class VMTranslator:
    SEG = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
        'temp': 5,
        'pointer': 3,
        'static': 16
    }

    @staticmethod
    def vm_push(segment, index):
        asm = []
        if segment == 'constant':
            asm += [f"@{index}", "D=A"]
        elif segment in ('local','argument','this','that'):
            base = VMTranslator.SEG[segment]
            asm += [f"@{base}", "D=M", f"@{index}", "A=D+A", "D=M"]
        elif segment in ('temp','pointer'):
            addr = VMTranslator.SEG[segment] + int(index)
            asm += [f"@{addr}", "D=M"]
        elif segment == 'static':
            addr = VMTranslator.SEG['static'] + int(index)
            asm += [f"@{addr}", "D=M"]
        asm += ["@SP","A=M","M=D","@SP","M=M+1"]
        return '\n'.join(asm)

    @staticmethod
    def vm_pop(segment, index):
        asm = []
        if segment in ('local','argument','this','that'):
            base = VMTranslator.SEG[segment]
            asm += [
                f"@{base}", "D=M", f"@{index}", "D=D+A", "@R13","M=D",
                "@SP","AM=M-1","D=M","@R13","A=M","M=D"
            ]
        elif segment in ('temp','pointer'):
            addr = VMTranslator.SEG[segment] + int(index)
            asm += ["@SP","AM=M-1","D=M",f"@{addr}","M=D"]
        elif segment == 'static':
            addr = VMTranslator.SEG['static'] + int(index)
            asm += ["@SP","AM=M-1","D=M",f"@{addr}","M=D"]
        return '\n'.join(asm)

    @staticmethod
    def vm_eq():
        # pop y; pop x; push (x==y ? -1 : 0)
        return '\n'.join([
            "@SP","AM=M-1","D=M",      # D=y
            "A=A-1","D=M-D",          # D=x-y
            "@EQ_TRUE","D;JEQ",       # if zero jump
            "@SP","A=M-1","M=0",      # else *SP-1 = false(0)
            "@EQ_END","0;JMP",
            "(EQ_TRUE)",
            "@SP","A=M-1","M=-1",     # true(-1)
            "(EQ_END)"
        ])

    @staticmethod
    def vm_gt():
        # pop y; pop x; push (x>y ? -1 : 0)
        return '\n'.join([
            "@SP","AM=M-1","D=M",      # D=y
            "A=A-1","D=M-D",          # D=x-y
            "@GT_TRUE","D;JGT",       # if >0 jump
            "@SP","A=M-1","M=0",      # else false
            "@GT_END","0;JMP",
            "(GT_TRUE)",
            "@SP","A=M-1","M=-1",     # true
            "(GT_END)"
        ])


if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: VMTranslator.py <file.vm>"); sys.exit(1)
    for line in open(sys.argv[1]):
        toks = line.strip().split()
        if not toks or toks[0].startswith("//"):
            continue
        cmd = toks[0]
        if cmd=="push":
            print(VMTranslator.vm_push(toks[1], toks[2]))
        elif cmd=="pop":
            print(VMTranslator.vm_pop(toks[1], toks[2]))
        elif cmd=="eq":
            print(VMTranslator.vm_eq())
        elif cmd=="gt":
            print(VMTranslator.vm_gt())
