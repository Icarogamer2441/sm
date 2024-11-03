import sys
import sm
import os

class TokenType:
    Int: str = "INTEGER"
    Float: str = "FLOAT"
    String: str = "STRING"
    Set: str = "SET"
    Id: str = "IDENTIFIER"
    Semicolon: str = "SEMICOLON"
    Lparen: str = "LPAREN"
    Rparen: str = "RPAREN"
    Plus: str = "PLUS"
    Minus: str = "MINUS"
    Times: str = "TIMES"
    Div: str = "DIVIDE"
    Colon: str = "COLON"
    Comment: str = "COMMENT"
    Mod: str = "MOD"
    Public: str = "PUBLICVAR"

def isint(s: str):
    try:
        int(s)
        return True
    except:
        return False

def isfloat(s: str):
    try:
        float(s)
        return True
    except:
        return False

def tokenize(code: str):
    tokens = []
    pos = 0
    while pos < len(code):
        char = code[pos]
        pos += 1

        if char.isdigit():
            final = ""
            while (char.isdigit() or char == ".") and pos < len(code):
                final += char

                char = code[pos]
                pos += 1
            if isint(final):
                tokens.append((TokenType.Int, int(final)))
            elif isfloat(final):
                tokens.append((TokenType.Float, float(final)))
            else:
                tokens.append((TokenType.Id, final))
            pos -= 1
        elif char == "\"":
            final = char
            char = code[pos]
            pos += 1
            while char != "\"" and pos < len(code):
                final += char
                char = code[pos]
                pos += 1
            final += char
            tokens.append((TokenType.String, final))
        elif char == ";":
            tokens.append((TokenType.Semicolon, char))
        elif char == "=":
            tokens.append((TokenType.Set, char))
        elif char == "(":
            tokens.append((TokenType.Lparen, char))
        elif char == ")":
            tokens.append((TokenType.Rparen, char))
        elif char in "\n\t \r":
            continue
        elif char == "+":
            tokens.append((TokenType.Plus, char))
        elif char == "-":
            tokens.append((TokenType.Minus, char))
        elif char == "*":
            tokens.append((TokenType.Times, char))
        elif char == "/":
            tokens.append((TokenType.Div, char))
        elif char == ":":
            tokens.append((TokenType.Colon, char))
        elif char == "#":
            final = char
            char = code[pos]
            pos += 1
            while char != "#" and pos < len(code):
                final += char

                char = code[pos]
                pos += 1
            final += char
            tokens.append((TokenType.Comment, final))
        elif char == "%":
            tokens.append((TokenType.Mod, char))
        elif char == "$":
            tokens.append((TokenType.Public, char))
        else:
            final = ""
            while pos < len(code) and not char in ";()\n \t\r\"=+-/*:%$":
                final += char

                char = code[pos]
                pos += 1
            if char in ";()\n \t\r\"=+-/*:$":
                pos -= 1
            elif char not in ";()\n \t\r\"=+-/*:$":
                final += char
            tokens.append((TokenType.Id, final))
    return tokens

def include(path: str):
    if os.name == "nt":
        path = os.path.join(os.environ["USERPROFILE"], "sminclude", path)
    else:
        path = os.path.join(os.environ["HOME"], "sminclude", path)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        code = f.read()
    if path.endswith(".ioasm"):
        ioasmcom(code)
    elif path.endswith(".iol"):
        comp1(code)

funcs = []
pvars = []

vm = sm.Vm()

defines = {}

def ioasmcom(code: str):
    lines = code.split("\n")
    for line in lines:
        parts = line.split()
        if len(parts):
            if parts[0] == "push":
                vm.push(defines[parts[1]] if parts[1] in defines.keys() else " ".join(parts[1:]))
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
                vm.var(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "ret":
                vm.ret()
            elif parts[0] == "call":
                vm.call(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "jmp":
                vm.jmp(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "eq":
                vm.eq(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "neq":
                vm.neq(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "gre":
                vm.greater(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "less":
                vm.less(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "geq":
                vm.geq(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "leq":
                vm.leq(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
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
            elif parts[0] == "exit":
                vm.exit()
            elif parts[0] == "prompt":
                vm.prompt()
            elif parts[0] == "toint":
                vm.toint()
            elif parts[0] == "tofloat":
                vm.tofloat()
            elif parts[0] == "tostr":
                vm.tostr()
            elif parts[0] == "rand":
                vm.rand()
            elif parts[0] == "list":
                vm.list()
            elif parts[0] == "append":
                vm.append()
            elif parts[0] == "lpop":
                vm.lpop()
            elif parts[0] == "public":
                vm.public(parts[1] if parts[1] not in defines.keys() else defines[parts[1]])
            elif parts[0] == "splits":
                vm.splits()
            elif parts[0] == "open":
                vm.openn()
            elif parts[0] == "write":
                vm.write()
            elif parts[0] == "read":
                vm.read()
            elif parts[0] == "readlines":
                vm.readlines()
            elif parts[0] == "close":
                vm.close()
            elif parts[0] == "reversed":
                vm.reversedd()
            elif parts[0] == "getidx":
                vm.getindex()
            elif parts[0] == "%define":
                defines[parts[1]] = " ".join(parts[2:])
            elif parts[0] == "halt":
                vm.halt()
            elif parts[0] == "band":
                vm.band()
            elif parts[0] == "bor":
                vm.bor()
            elif parts[0] == "shl":
                vm.shl()
            elif parts[0] == "shr":
                vm.shr()
            elif parts[0] == "popr":
                vm.popr(parts[1])
            elif parts[0] == "syscall":
                vm.syscall()
            elif parts[0] == "wait":
                vm.wait()
            elif parts[0] == "cmd":
                vm.cmd()
            elif parts[0] == "chdir":
                vm.chdir()
            else:
                print("Error: unknown instruction: {}".format(parts[0]))

def comp2(code: str, lvarss: list = []):
    lvars = lvarss
    toks = tokenize(code)
    pos = 0
    while pos < len(toks):
        token = toks[pos]
        pos += 1
        if token[0] == TokenType.Int or token[0] == TokenType.Float or token[0] == TokenType.String:
            vm.push(str(token[1]))
        elif token[0] == TokenType.Plus:
            vm.add()
        elif token[0] == TokenType.Minus:
            vm.sub()
        elif token[0] == TokenType.Times:
            vm.mul()
        elif token[0] == TokenType.Div:
            vm.div()
        elif token[0] == TokenType.Mod:
            vm.mod()
        elif token[0] == TokenType.Id:
            if token[1] == "print":
                vm.prt()
            elif token[1] in lvars:
                vm.push(token[1])
            elif token[1] in funcs:
                vm.call(token[1])
            elif token[1] == "return":
                vm.ret()
            elif token[1] == "jmp":
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.Id:
                    vm.jmp(token[1])
                else:
                    print("Error: use normal words to specify function name!")
                    sys.exit(1)
            elif token[1] == "dup":
                vm.dup()
            elif token[1] == "pop":
                vm.pop()
            elif token[1] == "swap":
                vm.swap()
            elif token[1] == "over":
                vm.over()
            elif token[1] == "exit":
                vm.exit()
            elif token[1] == "prompt":
                vm.prompt()
            elif token[1] == "toint":
                vm.toint()
            elif token[1] == "tofloat":
                vm.tofloat()
            elif token[1] == "tostr":
                vm.tostr()
            elif token[1] == "rand":
                vm.rand()
            elif token[1] == "equal":
                token = toks[pos]
                pos += 1
                vm.eq(token[1])
            elif token[1] == "notequal":
                token = toks[pos]
                pos += 1
                vm.neq(token[1])
            elif token[1] == "greater":
                token = toks[pos]
                pos += 1
                vm.greater(token[1])
            elif token[1] == "less":
                token = toks[pos]
                pos += 1
                vm.less(token[1])
            elif token[1] == "grequal":
                token = toks[pos]
                pos += 1
                vm.geq(token[1])
            elif token[1] == "lequal":
                token = toks[pos]
                pos += 1
                vm.leq(token[1])
            elif token[1] == "list":
                vm.list()
            elif token[1] == "append":
                vm.append()
            elif token[1] == "lpop":
                vm.lpop()
            elif token[1] in pvars:
                vm.push(token[1])
            elif token[1] == "exists":
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.Id:
                    pass
                else:
                    print("Error: Use identifiers to specify variables names!")
                    sys.exit(1)
                lvars.append(token[1])
            elif token[1] == "splits":
                vm.splits()
            elif token[1] == "open":
                vm.openn()
            elif token[1] == "write":
                vm.write()
            elif token[1] == "read":
                vm.read()
            elif token[1] == "readlines":
                vm.readlines()
            elif token[1] == "close":
                vm.close()
            elif token[1] == "reversed":
                vm.reversedd()
            elif token[1] == "getidx":
                vm.getindex()
            elif token[1] == "shl":
                vm.shl()
            elif token[1] == "shr":
                vm.shr()
            elif token[1] == "band":
                vm.band()
            elif token[1] == "bor":
                vm.bor()
            elif token[1] == "wait":
                vm.wait()
            elif token[1] == "cmd":
                vm.cmd()
            elif token[1] == "chandir":
                vm.chdir()
            else:
                print("Error: unknown variable/function or keyword -> '{}'".format(token[1]))
                sys.exit(1)
        elif token[0] == TokenType.Colon:
            token = toks[pos]
            pos += 1
            vname = ""
            if token[0] == TokenType.Id:
                vname = token[1]
            else:
                print("Error: use normal words to specify variable name!")
                sys.exit(1)
            vm.var(vname)
            lvars.append(vname)
        elif token[0] == TokenType.Comment:
            continue
        elif token[0] == TokenType.Public:
            token = toks[pos]
            pos += 1
            vname = ""
            if token[0] == TokenType.Id:
                vname = token[1]
            else:
                print("Error: use normal words to specify variable name!")
                sys.exit(1)
            vm.public(vname)
        else:
            print("Error: unknown token -> '{}'".format(token[1]))
            sys.exit(1)

def comp1(code: str):
    toks = tokenize(code)
    pos = 0
    while pos < len(toks):
        token = toks[pos]
        pos += 1
        if token[0] == TokenType.Id:
            if token[1] == "fn":
                token = toks[pos]
                pos += 1
                rettype = token[1]
                token = toks[pos]
                pos += 1
                fname = ""
                if token[0] == TokenType.Id:
                    fname = token[1]
                else:
                    print("Error: use normal words to specify function name!")
                    sys.exit(1)
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.Set:
                    vm.label(fname, rettype)
                    token = toks[pos]
                    pos += 1
                    finalcode = []
                    while token[0] != TokenType.Semicolon and pos < len(toks):
                        finalcode.append(str(token[1]))

                        token = toks[pos]
                        pos += 1
                    comp2(" ".join(finalcode))
                    funcs.append(fname)
                else:
                    print("Error: use '=' to start a function code block and ';' to end")
                    sys.exit(1)
            elif token[1] == "var":
                token = toks[pos]
                pos += 1
                vartype = token[1]
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.Id:
                    vname = token[1]
                else:
                    print("Error: use normal words to specify function name!")
                    sys.exit(1)
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.Set:
                    token = toks[pos]
                    pos += 1
                    finalcode = []
                    while token[0] != TokenType.Semicolon and pos < len(toks):
                        finalcode.append(str(token[1]))

                        token = toks[pos]
                        pos += 1
                    comp2(" ".join(finalcode))
                    pvars.append(vname)
                    vm.setType(vname, vartype)
                    vm.var(vname)
                    vm.public(vname)
                else:
                    print("Error: use '=' to start a variable value code block and ';' to end")
                    sys.exit(1)
            elif token[1] == "use":
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.String:
                    fname = token[1].replace("\"", "")
                    if fname.endswith(".iol"):
                        with open(fname, "r") as inp:
                            code = inp.read()
                        comp1(code)
                    elif fname.endswith(".ioasm"):
                        with open(fname, "r") as inp:
                            code = inp.read()
                        ioasmcom(code)
                    else:
                        print("Error: use '.iol' or '.ioasm' file extension to import it!")
                        sys.exit(1)
                else:
                    print("Error: use strings to specify your file")
                    sys.exit(1)
            elif token[1] == "funcExists":
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.Id:
                    fname = token[1]
                else:
                    print("Error: use normal words to specify function name!")
                    sys.exit(1)
                funcs.append(fname)
            elif token[1] == "varExists":
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.Id:
                    vname = token[1]
                else:
                    print("Error: use normal words to specify variable name!")
                    sys.exit(1)
                pvars.append(vname)
            elif token[1] == "include":
                token = toks[pos]
                pos += 1
                if token[0] == TokenType.String:
                    fname = token[1].replace("\"", "")
                    if fname.endswith(".iol"):
                        include(fname)
                    elif fname.endswith(".ioasm"):
                        include(fname)
                    else:
                        print("Error: use '.iol' or '.ioasm' file extension to import it!")
                        sys.exit(1)
                else:
                    print("Error: use strings to specify your file")
                    sys.exit(1)
            else:
                print("Error: unknown keyword -> {}".format(token[1]))
                sys.exit(1)
        elif token[0] == TokenType.Comment:
            continue
        else:
            print("Error: unknown token -> '{}'".format(token[1]))
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[1].endswith(".iol"):
            if "/" in sys.argv[1]:
                dir = "/".join(sys.argv[1].split("/")[0:-1])
                os.chdir(dir)
                fname = sys.argv[1].split("/")[-1]
            elif "\\" in sys.argv[1]:
                dir = "/".join(sys.argv[1].split("\\")[0:-1])
                os.chdir(dir)
                fname = sys.argv[1].split("\\")[-1]
            else:
                fname = sys.argv[1]
            outname = sys.argv[2]
            with open(fname, "r") as inp:
                code = inp.read()
            comp1(code)
            vm.compile(outname)
        else:
            print("Error: use '.iol' file extension!")
            sys.exit(1)
    else:
        print(f"Usage: {sys.argv[0]} <file.iol> <outname>")
        sys.exit(1)
