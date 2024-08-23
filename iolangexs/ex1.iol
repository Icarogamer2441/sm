fn void test =
	"This works!\n" print
	0 exit;

fn int main =
	jmp test
	#in case you remove the 'jmp test':#
	"This will not work!\n" print
	0 return;
