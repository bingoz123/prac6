// Fib03.tst — Test Fib.fib(6) ⇒ 8
load Fib.vm,
output-file Fib03.out,
compare-to Fib03.cmp,
output-list sp%D1.6.1 local%D1.6.1 argument%D1.8.1 this%D1.6.1 that%D1.6.1
            RAM[16]%D1.6.1 RAM[17]%D1.6.1;

set sp 256,
set local 300,
set argument 400,
set this 3000,
set that 3010,

set RAM[17] 6,    // static[1] = 6
set RAM[16] 0,

// give it enough steps for deep recursion
repeat 300 { vmstep; }
output;
