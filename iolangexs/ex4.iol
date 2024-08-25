fn void true =
    "Is true!\n" print
    0 exit;

fn void false =
    "is false!\n" print
    0 exit;

fn int main =
    # you can use: 'equal' = 'if (a b ==) {jmp label}', 'notequal' = 'if (a b !=) {jmp label}', 'greater' =
    'if (a b >) {jmp label}', 'less' = 'if (a b !=) {jmp label}', 'grequal' = 'if (a b >=) {jmp label}',
    'lequal' = 'if (a b <=) {jmp label}' #
    "a" "a" equal true
    jmp false
    0 return;
