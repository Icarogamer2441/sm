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

funcs = []
pvars = []

vm = sm.Vm()

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
                    else:
                        print("Error: use '.iol' file extension to import it!")
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
