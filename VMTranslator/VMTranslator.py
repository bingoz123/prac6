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
        # constant
        if segment == "constant":
            return f"""@{offset}
D=A
@SP
A=M
M=D
@SP
M=M+1"""

        # local, argument, this, that
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

        # temp  (mapped to RAM[5..12])
        if segment == "temp":
            addr = 5 + offset
            return f"""@{addr}
D=M
@SP
A=M
M=D
@SP
M=M+1"""

        # pointer 0->THIS, 1->THAT
        if segment == "pointer":
            sym = "THIS" if offset==0 else "THAT"
            return f"""@{sym}
D=M
@SP
A=M
M=D
@SP
M=M+1"""

        # static  (mapped to RAM[16..])
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
        # local, argument, this, that
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

        # temp
        if segment == "temp":
            addr = 5 + offset
            return f"""@SP
AM=M-1
D=M
@{addr}
M=D"""

        # pointer
        if segment == "pointer":
            sym = "THIS" if offset==0 else "THAT"
            return f"""@SP
AM=M-1
D=M
@{sym}
M=D"""

        # static
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
        """Generate Hack Assembly code for a VM add operation"""
        return """@SP
AM=M-1
D=M
A=A-1
M=M+D"""

    @staticmethod
    def vm_sub():
        """Generate Hack Assembly code for a VM sub operation"""
        return """@SP
AM=M-1
D=M
A=A-1
M=M-D"""

    @staticmethod
    def vm_neg():
        """Generate Hack Assembly code for a VM neg operation"""
        return """@SP
A=M-1
M=-M"""

    @staticmethod
    def vm_eq():
        """Generate Hack Assembly code for a VM eq operation"""
        label_true = VMTranslator._unique("EQ_TRUE")
        label_end  = VMTranslator._unique("EQ_END")
        return f"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@{label_true}
D;JEQ
@SP
A=M-1
M=0
@{label_end}
0;JMP
({label_true})
@SP
A=M-1
M=-1
({label_end})"""

    @staticmethod
    def vm_gt():
        """Generate Hack Assembly code for a VM gt operation"""
        label_true = VMTranslator._unique("GT_TRUE")
        label_end  = VMTranslator._unique("GT_END")
        return f"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@{label_true}
D;JGT
@SP
A=M-1
M=0
@{label_end}
0;JMP
({label_true})
@SP
A=M-1
M=-1
({label_end})"""

    @staticmethod
    def vm_lt():
        """Generate Hack Assembly code for a VM lt operation"""
        label_true = VMTranslator._unique("LT_TRUE")
        label_end  = VMTranslator._unique("LT_END")
        return f"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@{label_true}
D;JLT
@SP
A=M-1
M=0
@{label_end}
0;JMP
({label_true})
@SP
A=M-1
M=-1
({label_end})"""

    @staticmethod
    def vm_and():
        """Generate Hack Assembly code for a VM and operation"""
        return """@SP
AM=M-1
D=M
A=A-1
M=M&D"""

    @staticmethod
    def vm_or():
        """Generate Hack Assembly code for a VM or operation"""
        return """@SP
AM=M-1
D=M
A=A-1
M=M|D"""

    @staticmethod
    def vm_not():
        """Generate Hack Assembly code for a VM not operation"""
        return """@SP
A=M-1
M=!M"""

    # The following are *not* required for Part 4—stubbed out:
    @staticmethod
    def vm_label(label):      return ""
    @staticmethod
    def vm_goto(label):       return ""
    @staticmethod
    def vm_if(label):         return ""
    @staticmethod
    def vm_function(fn, n):   return ""
    @staticmethod
    def vm_return():          return ""
    @staticmethod
    def vm_call(fn, n):       return ""

# standalone driver (VM→ASM)
if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: VMTranslator.py <file.vm>")
        sys.exit(1)
    path = sys.argv[1]
    for raw in open(path):
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        toks = line.split()
        cmd = toks[0].lower()
        if cmd=="push":
            print(VMTranslator.vm_push(toks[1], int(toks[2])))
        elif cmd=="pop":
            print(VMTranslator.vm_pop(toks[1], int(toks[2])))
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
        # ignore other commands
