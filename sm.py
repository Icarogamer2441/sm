class OpType:
    Push: int = 0
    Pop: int = 1
    Add: int = 2
    Sub: int = 3
    Mul: int = 4
    Div: int = 5
    Label: int = 6
    Print: int = 7
    Mod: int = 8
    Var: int = 9
    Ret: int = 10
    Call: int = 11
    Jump: int = 12
    Equal: int = 13
    NEqual: int = 14
    Greater: int = 15
    Less: int = 16
    GEqual: int = 17
    LEqual: int = 18
    Dup: int = 19
    Swap: int = 20
    Over: int = 21
    SetType: int = 22
    Exit: int = 23
    Prompt: int = 24
    Toint: int = 25
    Tofloat: int = 26
    Tostr: int = 27
    Rand: int = 28
    List: int = 29
    Append: int = 30
    Lpop: int = 31
    Public: int = 32

class Vm:
    def __init__(self):
        self.bytecode = bytearray()

    def push(self, value: str):
        self.bytecode.append(OpType.Push)
        self.bytecode.append(len(value))
        self.bytecode.extend(value.encode("utf-8"))

    def pop(self):
        self.bytecode.append(OpType.Pop)

    def add(self):
        self.bytecode.append(OpType.Add)

    def sub(self):
        self.bytecode.append(OpType.Sub)

    def mul(self):
        self.bytecode.append(OpType.Mul)

    def div(self):
        self.bytecode.append(OpType.Div)

    def label(self, name: str, typ: str):
        self.bytecode.append(OpType.Label)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))
        if typ == "int":
            self.bytecode.append(0)
        elif typ == "float":
            self.bytecode.append(1)
        elif typ == "string":
            self.bytecode.append(2)
        elif typ == "void":
            self.bytecode.append(3)
        elif typ == "list":
            self.bytecode.append(4)
        else:
            print("Error: unknown function return type: {}".format(typ))

    def prt(self):
        self.bytecode.append(OpType.Print)

    def mod(self):
        self.bytecode.append(OpType.Mod)

    def var(self, name: str):
        self.bytecode.append(OpType.Var)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def ret(self):
        self.bytecode.append(OpType.Ret)

    def call(self, name: str):
        self.bytecode.append(OpType.Call)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def jmp(self, name: str):
        self.bytecode.append(OpType.Jump)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def eq(self, name: str):
        self.bytecode.append(OpType.Equal)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def neq(self, name: str):
        self.bytecode.append(OpType.NEqual)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def greater(self, name: str):
        self.bytecode.append(OpType.Greater)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def less(self, name: str):
        self.bytecode.append(OpType.Less)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def geq(self, name: str):
        self.bytecode.append(OpType.GEqual)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def leq(self, name: str):
        self.bytecode.append(OpType.LEqual)
        self.bytecode.append(len(name))
        self.bytecode.extend(name.encode("utf-8"))

    def dup(self):
        self.bytecode.append(OpType.Dup)

    def swap(self):
        self.bytecode.append(OpType.Swap)

    def over(self):
        self.bytecode.append(OpType.Over)

    def setType(self, var: str, typ: str):
        self.bytecode.append(OpType.SetType)
        self.bytecode.append(len(var))
        self.bytecode.extend(var.encode("utf-8"))
        if typ == "int":
            self.bytecode.append(0)
        elif typ == "float":
            self.bytecode.append(1)
        elif typ == "string":
            self.bytecode.append(2)
        elif typ == "list":
            self.bytecode.append(3)
        else:
            print("Error: unknown variable type: {}".format(typ))

    def exit(self):
        self.bytecode.append(OpType.Exit)

    def prompt(self):
        self.bytecode.append(OpType.Prompt)

    def toint(self):
        self.bytecode.append(OpType.Toint)

    def tofloat(self):
        self.bytecode.append(OpType.Tofloat)

    def tostr(self):
        self.bytecode.append(OpType.Tostr)

    def rand(self):
        self.bytecode.append(OpType.Rand)
    
    def list(self):
        self.bytecode.append(OpType.List)
    
    def append(self):
        self.bytecode.append(OpType.Append)
    
    def lpop(self):
        self.bytecode.append(OpType.Lpop)

    def public(self, varname: str):
        self.bytecode.append(OpType.Public)
        self.bytecode.append(len(varname))
        self.bytecode.extend(varname.encode("utf-8"))

    def compile(self, out: str):
        with open(out + ".sm", "wb") as f:
            f.write(self.bytecode)
