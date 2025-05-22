#!/usr/bin/env python3
import sys

class VMTranslator:
    label_counter = 0

    @staticmethod
    def unique(label):
        VMTranslator.label_counter += 1
        return f"{label}${VMTranslator.label_counter}"

    @staticmethod
    def vm_add():
        return "\n".join([
            "@SP",      # SP--
            "AM=M-1",   #   SP = SP-1; A = SP
            "D=M",      #   D = *SP  (y)
            "A=A-1",    #   A = SP-1 (address of x)
            "M=M+D"     #   * (SP-1) = x + y
        ])

    @staticmethod
    def vm_sub():
        return "\n".join([
            "@SP",
            "AM=M-1",
            "D=M",      # D = y
            "A=A-1",
            "M=M-D"     # x - y
        ])

    @staticmethod
    def vm_neg():
        return "\n".join([
            "@SP",
            "A=M-1",    # A = SP-1
            "M=-M"      # *SP = -*SP
        ])

    @staticmethod
    def vm_eq():
        t = VMTranslator.unique("EQ_TRUE")
        e = VMTranslator.unique("EQ_END")
        return "\n".join([
            "@SP",
            "AM=M-1",
            "D=M",      # D = y
            "A=A-1",
            "D=M-D",    # x - y
            f"@{t}",
            "D;JEQ",    # if zero, jump EQ_TRUE
            "@SP",
            "A=M-1",
            "M=0",      # false
            f"@{e}",
            "0;JMP",
            f"({t})",
            "@SP",
            "A=M-1",
            "M=-1",     # true
            f"({e})"
        ])

    @staticmethod
    def vm_gt():
        t = VMTranslator.unique("GT_TRUE")
        e = VMTranslator.unique("GT_END")
        return "\n".join([
            "@SP",
            "AM=M-1",
            "D=M",      # D = y
            "A=A-1",
            "D=M-D",    # x - y
            f"@{t}",
            "D;JGT",    # if >0
            "@SP",
            "A=M-1",
            "M=0",
            f"@{e}",
            "0;JMP",
            f"({t})",
            "@SP",
            "A=M-1",
            "M=-1",
            f"({e})"
        ])

    @staticmethod
    def vm_lt():
        t = VMTranslator.unique("LT_TRUE")
        e = VMTranslator.unique("LT_END")
        return "\n".join([
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "D=M-D",
            f"@{t}",
            "D;JLT",
            "@SP",
            "A=M-1",
            "M=0",
            f"@{e}",
            "0;JMP",
            f"({t})",
            "@SP",
            "A=M-1",
            "M=-1",
            f"({e})"
        ])

    @staticmethod
    def vm_and():
        return "\n".join([
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "M=M&D"
        ])

    @staticmethod
    def vm_or():
        return "\n".join([
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "M=M|D"
        ])

    @staticmethod
    def vm_not():
        return "\n".join([
            "@SP",
            "A=M-1",
            "M=!M"
        ])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: VMTranslator.py <file.vm>")
        sys.exit(1)

    for raw in open(sys.argv[1]):
        line = raw.split("//")[0].strip()
        if not line: continue
        cmd, *args = line.split()
        if cmd == "add":
            print(VMTranslator.vm_add())
        elif cmd == "sub":
            print(VMTranslator.vm_sub())
        elif cmd == "neg":
            print(VMTranslator.vm_neg())
        elif cmd == "eq":
            print(VMTranslator.vm_eq())
        elif cmd == "gt":
            print(VMTranslator.vm_gt())
        elif cmd == "lt":
            print(VMTranslator.vm_lt())
        elif cmd == "and":
            print(VMTranslator.vm_and())
        elif cmd == "or":
            print(VMTranslator.vm_or())
        elif cmd == "not":
            print(VMTranslator.vm_not())
        # ignore push/pop/flow for this task
