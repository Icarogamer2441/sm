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

```console
$ python ./build.py all
$ ./dist/iolang ./iolangexs/ex1.iol outname
```