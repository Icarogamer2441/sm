fn void test =
   exists n1 #this is used to tell the compiler that the variable n1 is in other functions but it's public#
   n1 print "\n" print;

fn int main =
   10 :n1 $n1 #this makes it public#
   test
   0 return;