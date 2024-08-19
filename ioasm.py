import sm
import sys

vm = sm.Vm()

def compiler(code: str):
    lines = code.split("\n")
    for line in lines:
        parts = line.split()
        if len(parts):
            if parts[0] == "push":
                vm.push(" ".join(parts[1:]))
            elif parts[0] == "pop":
                vm.pop()
            elif parts[0] == "add":
                vm.add()
            elif parts[0] == "sub":
                vm.sub()
            elif parts[0] == "mul":
                vm.mul()
            elif parts[0] == "div":
                vm.div()
            elif parts[0].endswith(":"):
                vm.label(parts[0][:-1], parts[1])
            elif parts[0] == "print":
                vm.prt()
            elif parts[0] == "mod":
                vm.mod()
            elif parts[0] == "var":
                vm.var(parts[1])
            elif parts[0] == "ret":
                vm.ret()
            elif parts[0] == "call":
                vm.call(parts[1])
            elif parts[0] == "jmp":
                vm.jmp(parts[1])
            elif parts[0] == "eq":
                vm.eq(parts[1])
            elif parts[0] == "neq":
                vm.neq(parts[1])
            elif parts[0] == "gre":
                vm.greater(parts[1])
            elif parts[0] == "less":
                vm.less(parts[1])
            elif parts[0] == "geq":
                vm.geq(parts[1])
            elif parts[0] == "leq":
                vm.leq(parts[1])
            elif parts[0] == "dup":
                vm.dup()
            elif parts[0] == "swap":
                vm.swap()
            elif parts[0] == "over":
                vm.over()
            elif parts[0].startswith(";"):
                pass
            elif parts[0] == "vtype":
                vm.setType(parts[1], parts[2])
            else:
                print("Error: unknown instruction: {}".format(parts[0]))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[1].endswith(".ioasm"):
            with open(sys.argv[1], "r") as inp:
                code = inp.read()
            compiler(code)
            vm.compile(sys.argv[2])
        else:
            print("Error: use '.ioasm' extension")
            sys.exit(1)
    else:
        print(f"Usage: {sys.argv[0]} <filename.ioasm> <outname>")
        sys.exit(1)
