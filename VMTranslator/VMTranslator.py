#!/usr/bin/env python3
import sys

class VMTranslator:
    # used to generate unique labels for eq/gt/lt
    label_count = 0

    @staticmethod
    def _unique(prefix):
        VMTranslator.label_count += 1
        return f"{prefix}${VMTranslator.label_count}"

    @staticmethod
    def vm_push(segment, offset):
        """Generate Hack Assembly code for a VM push operation"""
        if segment == "constant":
            return f"""@{offset}
D=A
@SP
A=M
M=D
@SP
M=M+1"""

        if segment in ("local","argument","this","that"):
            base = {"local":"LCL","argument":"ARG","this":"THIS","that":"THAT"}[segment]
            return f"""@{offset}
D=A
@{base}
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1"""

        if segment == "temp":
            addr = 5 + offset
            return f"""@{addr}
D=M
@SP
A=M
M=D
@SP
M=M+1"""

        if segment == "pointer":
            sym = "THIS" if offset==0 else "THAT"
            return f"""@{sym}
D=M
@SP
A=M
M=D
@SP
M=M+1"""

        if segment == "static":
            return f"""@16
D=A
@{offset}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1"""

        raise ValueError(f"vm_push: unknown segment '{segment}'")

    @staticmethod
    def vm_pop(segment, offset):
        """Generate Hack Assembly code for a VM pop operation"""
        if segment in ("local","argument","this","that"):
            base = {"local":"LCL","argument":"ARG","this":"THIS","that":"THAT"}[segment]
            return f"""@{offset}
D=A
@{base}
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D"""

        if segment == "temp":
            addr = 5 + offset
            return f"""@SP
AM=M-1
D=M
@{addr}
M=D"""

        if segment == "pointer":
            sym = "THIS" if offset==0 else "THAT"
            return f"""@SP
AM=M-1
D=M
@{sym}
M=D"""

        if segment == "static":
            return f"""@16
D=A
@{offset}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D"""

        if segment == "constant":
            raise ValueError("Cannot pop to constant")

        raise ValueError(f"vm_pop: unknown segment '{segment}'")

    @staticmethod
    def vm_add():
        return """@SP
AM=M-1
D=M
A=A-1
M=M+D"""

    @staticmethod
    def vm_sub():
        return """@SP
AM=M-1
D=M
A=A-1
M=M-D"""

    @staticmethod
    def vm_neg():
        return """@SP
A=M-1
M=-M"""

    @staticmethod
    def vm_eq():
        t = VMTranslator._unique("EQ_TRUE")
        e = VMTranslator._unique("EQ_END")
        return f"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@{t}
D;JEQ
@SP
A=M-1
M=0
@{e}
0;JMP
({t})
@SP
A=M-1
M=-1
({e})"""

    @staticmethod
    def vm_gt():
        t = VMTranslator._unique("GT_TRUE")
        e = VMTranslator._unique("GT_END")
        return f"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@{t}
D;JGT
@SP
A=M-1
M=0
@{e}
0;JMP
({t})
@SP
A=M-1
M=-1
({e})"""

    @staticmethod
    def vm_lt():
        t = VMTranslator._unique("LT_TRUE")
        e = VMTranslator._unique("LT_END")
        return f"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@{t}
D;JLT
@SP
A=M-1
M=0
@{e}
0;JMP
({t})
@SP
A=M-1
M=-1
({e})"""

    @staticmethod
    def vm_and():
        return """@SP
AM=M-1
D=M
A=A-1
M=M&D"""

    @staticmethod
    def vm_or():
        return """@SP
AM=M-1
D=M
A=A-1
M=M|D"""

    @staticmethod
    def vm_not():
        return """@SP
A=M-1
M=!M"""

    # --- Jump operations (4.4) ---
    @staticmethod
    def vm_label(label):
        # define a label in ASM
        return f"({label})"

    @staticmethod
    def vm_goto(label):
        # unconditional jump
        return f"""@{label}
0;JMP"""

    @staticmethod
    def vm_if(label):
        # pop top of stack; if != 0 jump
        return f"""@SP
AM=M-1
D=M
@{label}
D;JNE"""

    # the rest are stubbed out for now
    @staticmethod
    def vm_function(fn, n):   return ""
    @staticmethod
    def vm_call(fn, n):       return ""
    @staticmethod
    def vm_return():          return ""

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: VMTranslator.py <file.vm>")
        sys.exit(1)
    for raw in open(sys.argv[1]):
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        parts = line.split()
        cmd = parts[0]
        if cmd=="push":
            print(VMTranslator.vm_push(parts[1], int(parts[2])))
        elif cmd=="pop":
            print(VMTranslator.vm_pop(parts[1], int(parts[2])))
        elif cmd=="add":
            print(VMTranslator.vm_add())
        elif cmd=="sub":
            print(VMTranslator.vm_sub())
        elif cmd=="neg":
            print(VMTranslator.vm_neg())
        elif cmd=="eq":
            print(VMTranslator.vm_eq())
        elif cmd=="gt":
            print(VMTranslator.vm_gt())
        elif cmd=="lt":
            print(VMTranslator.vm_lt())
        elif cmd=="and":
            print(VMTranslator.vm_and())
        elif cmd=="or":
            print(VMTranslator.vm_or())
        elif cmd=="not":
            print(VMTranslator.vm_not())
        elif cmd=="label":
            print(VMTranslator.vm_label(parts[1]))
        elif cmd=="goto":
            print(VMTranslator.vm_goto(parts[1]))
        elif cmd=="if-goto":
            print(VMTranslator.vm_if(parts[1]))
        # ignore other commands
