# sm

Means Simple stack-based Machine

## quick start

if you don't have, install pyinstaller python package to compile this project:
```console
$ pip install pyinstaller
```

```console
$ make && sudo make install
```

compiling the [hello world file](./examples/hello.ioasm):
```console
$ ioasm ./examples/hello.ioasm outputname
```

executing the compiled code

```console
$ smrun outputname.sm
```

compiling the [iolang example file](./examples.iol):
```console
$ iolang ./examples.iol outname
```

## compiling the language on windows

you will need to install the following package:
```console
$ pip install pyinstaller
```

to compile, use:
```console
$ python ./build.py all
$ ./dist/iolang ./iolangexs/ex1.iol outname
```

## changing sm register mode

type 0 (default type):
```console
$ smrun myfile.sm -t0
```

type 1 (need to specify):
```console
$ smrun myfile.sm -t1
```

## includes

now you can use include (but only in iolang)
like this:
```iolang
# example: #
include "test1.iol"
include "test2.ioasm"

# you don't need to use funcExists or varExists with .iol files because it imports everything to the file #
varExists hello2

# your libraries for include will be in your user directory like this: $(userdir)/sminclude/ #

fn int main =
    hello1 print
    hello2 print
    0 return;
```

## set max memory

to you set your max memory you can use:

```console
$ smrun myfile.sm -mm <memory count>
```

or:

```console
$ smrun myfile.sm --max-memory <memory count>
```

## about memory

the memory will create a limit to the stack and the variables.

```python
stacksize = int(memory / 2)
memory = memory - stacksize
maxvars = int(memory)
```