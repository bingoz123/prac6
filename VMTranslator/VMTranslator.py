class VMTranslator:
    segment_pointers = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
        'temp': 5,
        'pointer': 3,
        'static': 16
    }

    @staticmethod
    def vm_push(segment, offset):
        asm = []
        if segment == 'constant':
            asm = [f"@{offset}", "D=A"]
        elif segment in ('local', 'argument', 'this', 'that'):
            asm = [
                f"@{VMTranslator.segment_pointers[segment]}", "D=M",
                f"@{offset}", "A=D+A", "D=M"
            ]
        elif segment == 'temp' or segment == 'pointer':
            asm = [f"@{VMTranslator.segment_pointers[segment] + int(offset)}", "D=M"]
        elif segment == 'static':
            asm = [f"@{VMTranslator.segment_pointers['static'] + int(offset)}", "D=M"]
        
        asm += ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        return '\n'.join(asm)

    @staticmethod
    def vm_pop(segment, offset):
        asm = []
        if segment in ('local', 'argument', 'this', 'that'):
            asm = [
                f"@{VMTranslator.segment_pointers[segment]}", "D=M",
                f"@{offset}", "D=D+A", "@R13", "M=D",  
                "@SP", "AM=M-1", "D=M",
                "@R13", "A=M", "M=D"
            ]
        elif segment == 'temp' or segment == 'pointer':
            asm = [
                "@SP", "AM=M-1", "D=M",
                f"@{VMTranslator.segment_pointers[segment] + int(offset)}", "M=D"
            ]
        elif segment == 'static':
            asm = [
                "@SP", "AM=M-1", "D=M",
                f"@{VMTranslator.segment_pointers['static'] + int(offset)}", "M=D"
            ]

        return '\n'.join(asm)

    @staticmethod
    def vm_add():
        asm = [
            "@SP", "AM=M-1", "D=M",
            "A=A-1", "M=M+D"
        ]
        return '\n'.join(asm)


# 主程序执行
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as file:
            for line in file:
                tokens = line.strip().split()
                if len(tokens) == 3 and tokens[0] == "push":
                    print(VMTranslator.vm_push(tokens[1], int(tokens[2])))
                elif len(tokens) == 3 and tokens[0] == "pop":
                    print(VMTranslator.vm_pop(tokens[1], int(tokens[2])))
                elif tokens[0] == "add":
                    print(VMTranslator.vm_add())
