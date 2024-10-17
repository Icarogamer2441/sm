use "regs.ioasm"

funcExists getsar
funcExists tosar
funcExists printwnl

fn int main =
    getsar printwnl "Hello world!\n" tosar
    getsar print
    0 return;