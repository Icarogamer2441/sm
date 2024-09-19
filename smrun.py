import sm
import sys
import random

Types = sm.OpType()

def is_int(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s: str):
    try:
        float(s)
        return True
    except:
        return False

def is_string(s: str):
    if s.startswith('"') and s.endswith('"'):
        return True
    return False

stack = []

for i, arg in enumerate(reversed(sys.argv[1:])):
    if i == len(sys.argv[1:]):
        continue
    else:
        stack.append(arg)
stack.append(len(sys.argv[1:]))

labels = {}

ret_types = ["int", "float", "string", "void", "list"]
var_types = ["int", "float", "string", "list"]
vars_types = {}
pvars = {}

def interpret(bytecode: bytearray, lvarss: dict = {},
                ret_type: str = "void", label_name: str = "program"):
    lvars = lvarss
    pos = 0
    lname = ""
    open_file = None
    while pos < len(bytecode):
        op = bytecode[pos]
        pos += 1
        if op == Types.Push:
            length = bytecode[pos]
            pos += 1
            value = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.Push)
                labels[lname][1].append(length)
                labels[lname][1].extend(value.encode("utf-8"))
            else:
                if is_int(value):
                    stack.append(int(value))
                elif is_float(value):
                    stack.append(float(value))
                elif is_string(value):
                    stack.append(value[1:len(value) - 1].replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\b", "\b"))
                elif value in lvars.keys():
                    stack.append(lvars[value])
                elif value in pvars.keys():
                    stack.append(pvars[value])
                else:
                    print("Error: unknown variable -> '{}'".format(value))
                    sys.exit(1)
        elif op == Types.Pop:
            if len(lname):
                labels[lname][1].append(Types.Pop)
            else:
                stack.pop()
        elif op == Types.Add:
            if len(lname):
                labels[lname][1].append(Types.Add)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        elif op == Types.Sub:
            if len(lname):
                labels[lname][1].append(Types.Sub)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
        elif op == Types.Mul:
            if len(lname):
                labels[lname][1].append(Types.Mul)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
        elif op == Types.Div:
            if len(lname):
                labels[lname][1].append(Types.Div)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(a / b)
        elif op == Types.Label:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            ret_typ = bytecode[pos]
            pos += 1
            labels[name] = [ret_types[ret_typ], bytearray()]
            lname = name
        elif op == Types.Print:
            if len(lname):
                labels[lname][1].append(Types.Print)
            else:
                print(stack.pop(), end="")
        elif op == Types.Mod:
            if len(lname):
                labels[lname][1].append(Types.Mod)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(a % b)
        elif op == Types.Var:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.Var)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                lvars[name] = stack.pop()
        elif op == Types.Ret:
            if len(lname):
                labels[lname][1].append(Types.Ret)
            else:
                if label_name == "main":
                    ret_value = stack.pop()
                    if isinstance(ret_value, int):
                        sys.exit(ret_value)
                    else:
                        print("Error: unknown use int to return main label value (main always need to return int values) -> '{}'".format(ret_type))
                        sys.exit(1)
                else:
                    ret_value = 0
                    if ret_type == "void":
                        pass
                    elif ret_type == "int":
                        ret_value = stack.pop()
                        if isinstance(ret_value, int):
                            stack.append(ret_value)
                        else:
                            print("Error: unknown use int to return value -> '{}'".format(ret_type))
                            sys.exit(1)
                    elif ret_type == "float":
                        ret_value = stack.pop()
                        if isinstance(ret_value, float):
                            stack.append(ret_value)
                        else:
                            print("Error: unknown use float to return value -> '{}'".format(ret_type))
                            sys.exit(1)
                    elif ret_type == "string":
                        ret_value = stack.pop()
                        if isinstance(ret_value, str):
                            stack.append(ret_value)
                        else:
                            print("Error: unknown use string to return value -> '{}'".format(ret_type))
                            sys.exit(1)
                    elif ret_type == "list":
                        ret_value = stack.pop()
                        if isinstance(ret_value, list):
                            stack.append(ret_value)
                        else:
                            print("Error: unknown use list to return value -> '{}'".format(ret_type))
                            sys.exit(1)
                    else:
                        print("Error: unknown return type -> '{}'".format(ret_type))
                        sys.exit(1)
                    break
        elif op == Types.Call:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.Call)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                if name in list(labels.keys()):
                    interpret(labels[name][1], label_name=name, ret_type=labels[name][0])
                else:
                    print("Error: unknown label -> '{}'".format(name))
                    sys.exit(1)
        elif op == Types.Jump:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.Jump)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                if name in list(labels.keys()):
                    interpret(labels[name][1], lvarss=lvars, ret_type=labels[name][0], label_name=name)
                    break
                else:
                    print("Error: unknown label -> '{}'".format(name))
                    sys.exit(1)
        elif op == Types.Equal:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.Equal)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                b = stack.pop()
                a = stack.pop()
                if a == b:
                    interpret(labels[name][1], lvars, labels[name][0], label_name=name)
                    break
                else:
                    pass
        elif op == Types.NEqual:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.NEqual)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                b = stack.pop()
                a = stack.pop()
                if a != b:
                    interpret(labels[name][1], lvars, labels[name][0], label_name=name)
                    break
                else:
                    pass
        elif op == Types.Greater:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.Greater)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                b = stack.pop()
                a = stack.pop()
                if a > b:
                    interpret(labels[name][1], lvars, labels[name][0], label_name=name)
                    break
                else:
                    pass
        elif op == Types.Less:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.Less)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                b = stack.pop()
                a = stack.pop()
                if a < b:
                    interpret(labels[name][1], lvars, labels[name][0], label_name=name)
                    break
                else:
                    pass
        elif op == Types.GEqual:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.GEqual)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                b = stack.pop()
                a = stack.pop()
                if a >= b:
                    interpret(labels[name][1], lvars, labels[name][0], label_name=name)
                    break
                else:
                    pass
        elif op == Types.LEqual:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.LEqual)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                b = stack.pop()
                a = stack.pop()
                if a <= b:
                    interpret(labels[name][1], lvars, labels[name][0], label_name=name)
                    break
                else:
                    pass
        elif op == Types.Dup:
            if len(lname):
                labels[lname][1].append(Types.Dup)
            else:
                stack.append(stack[-1])
        elif op == Types.Swap:
            if len(lname):
                labels[lname][1].append(Types.Swap)
            else:
                a = stack.pop()
                b = stack.pop()
                stack.append(a)
                stack.append(b)
        elif op == Types.Over:
            if len(lname):
                labels[lname][1].append(Types.Over)
            else:
                stack.append(stack[-2])
        elif op == Types.SetType:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            typ = bytecode[pos]
            pos += 1
            if len(lname):
                labels[lname][1].append(Types.SetType)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
                labels[lname][1].append(typ)
            else:
                vars_types[name] = var_types[typ]
        elif op == Types.Exit:
            if len(lname):
                labels[lname][1].append(Types.Exit)
            else:
                sys.exit(stack.pop())
        elif op == Types.Prompt:
            if len(lname):
                labels[lname][1].append(Types.Prompt)
            else:
                stack.append(input())
        elif op == Types.Toint:
            if len(lname):
                labels[lname][1].append(Types.Toint)
            else:
                a = stack.pop()
                stack.append(int(a))
        elif op == Types.Tofloat:
            if len(lname):
                labels[lname][1].append(Types.Tofloat)
            else:
                a = stack.pop()
                stack.append(float(a))
        elif op == Types.Tostr:
            if len(lname):
                labels[lname][1].append(Types.Tostr)
            else:
                a = stack.pop()
                stack.append(str(a))
        elif op == Types.Rand:
            if len(lname):
                labels[lname][1].append(Types.Rand)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(random.randint(a, b))
        elif op == Types.List:
            if len(lname):
                labels[lname][1].append(Types.List)
            else:
                stack.append([])
        elif op == Types.Append:
            if len(lname):
                labels[lname][1].append(Types.Append)
            else:
                lst = stack.pop()
                lst.append(stack.pop())
                stack.append(lst)
        elif op == Types.Lpop:
            if len(lname):
                labels[lname][1].append(Types.Lpop)
            else:
                lst = stack.pop()
                stack.append(lst.pop())
                stack.append(lst)
        elif op == Types.Public:
            length = bytecode[pos]
            pos += 1
            name = bytecode[pos:pos + length].decode("utf-8")
            pos += length
            if len(lname):
                labels[lname][1].append(Types.Public)
                labels[lname][1].append(length)
                labels[lname][1].extend(name.encode("utf-8"))
            else:
                if name in lvars.keys():
                    pvars[name] = lvars.pop(name)
                else:
                    print("Error: unknown local variable: '{}'".format(name))
                    sys.exit(1)
        elif op == Types.Splits:
            if len(lname):
                labels[lname][1].append(Types.Splits)
            else:
                item = stack.pop()
                if isinstance(item, int) or isinstance(item, float) or isinstance(item, list) or isinstance(item, dict):
                    stack.append(list(str(item)))
                else:
                    stack.append(item.split())
        elif op == Types.OpenFile:
            if len(lname):
                labels[lname][1].append(Types.OpenFile)
            else:
                # otype filename <keyword: open>
                fname = stack.pop()
                opentype = stack.pop()
                open_file = open(fname, opentype)
        elif op == Types.Write:
            if len(lname):
                labels[lname][1].append(Types.Write)
            else:
                # content <keyword: write>
                if open_file != None:
                    open_file.write(stack.pop())
                else:
                    print("Error: no file openeded!")
                    sys.exit(1)
        elif op == Types.Read:
            if len(lname):
                labels[lname][1].append(Types.Read)
            else:
                # content <keyword: read>
                if open_file != None:
                    stack.append(open_file.read())
                else:
                    print("Error: no file openeded!")
                    sys.exit(1)
        elif op == Types.ReadLines:
            if len(lname):
                labels[lname][1].append(Types.ReadLines)
            else:
                # content <keyword: readlines>
                if open_file != None:
                    stack.append(open_file.readlines())
                else:
                    print("Error: no file openeded!")
                    sys.exit(1)
        elif op == Types.Close:
            if len(lname):
                labels[lname][1].append(Types.ReadLines)
            else:
                # content <keyword: close>
                if open_file != None:
                    open_file.close()
                    open_file = None
                else:
                    print("Error: no file openeded!")
                    sys.exit(1)
        else:
            print("Error: unknown opcode: '{}', label name: '{}'".format(op, label_name))
            sys.exit(1)

        for var in list(lvars.keys()):
            if var in vars_types.keys():
                if vars_types[var] == "int":
                    if isinstance(lvars[var], int):
                        pass
                    else:
                        print("Error: variable '{}' is not int, label name: '{}'".format(var, label_name))
                        sys.exit(1)
                elif vars_types[var] == "float":
                    if isinstance(lvars[var], float):
                        pass
                    else:
                        print("Error: variable '{}' is not float, label name: '{}'".format(var, label_name))
                        sys.exit(1)
                elif vars_types[var] == "string":
                    if isinstance(lvars[var], str):
                        pass
                    else:
                        print("Error: variable '{}' is not string, label name: '{}'".format(var, label_name))
                        sys.exit(1)
                elif vars_types[var] == "list":
                    if isinstance(lvars[var], list):
                        pass
                    else:
                        print("Error: variable '{}' is not list, label name: '{}'".format(var, label_name))
                        sys.exit(1)
                else:
                    print("Error: unknown type: '{}', label name: '{}'".format(vars_types[var], label_name))
                    exit(1)
            else:
                pass
            
        for var in list(pvars.keys()):
            if var in vars_types.keys():
                if vars_types[var] == "int":
                    if isinstance(pvars[var], int):
                        pass
                    else:
                        print("Error: variable '{}' is not int, label name: '{}'".format(var, label_name))
                        sys.exit(1)
                elif vars_types[var] == "float":
                    if isinstance(pvars[var], float):
                        pass
                    else:
                        print("Error: variable '{}' is not float, label name: '{}'".format(var, label_name))
                        sys.exit(1)
                elif vars_types[var] == "string":
                    if isinstance(pvars[var], str):
                        pass
                    else:
                        print("Error: variable '{}' is not string, label name: '{}'".format(var, label_name))
                        sys.exit(1)
                elif vars_types[var] == "list":
                    if isinstance(pvars[var], list):
                        pass
                    else:
                        print("Error: variable '{}' is not list, label name: '{}'".format(var, label_name))
                        sys.exit(1)
                else:
                    print("Error: unknown type: '{}', label name: '{}'".format(vars_types[var], label_name))
                    exit(1)
            else:
                pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].endswith(".sm"):
            with open(sys.argv[1], "rb") as inp:
                code = inp.read()
            interpret(code)

            if "main" in list(labels.keys()):
                interpret(labels["main"][1], label_name="main", ret_type=labels["main"][0])
            print("Segmentation fault. use 'exit' in any function or 'push 0\nret' in main function to exit the program successfully")
            sys.exit(1)
        else:
            print("Error: use '.sm' extension")
            sys.exit(1)
    else:
        print(f"Usage: {sys.argv[0]} <filename.sm>")
        sys.exit(1)
