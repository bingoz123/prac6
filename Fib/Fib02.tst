// Fib02.tst — Test Fib.fib(1) ⇒ 1
load Fib.vm,
output-file Fib02.out,
compare-to Fib02.cmp,
output-list sp%D1.6.1 local%D1.6.1 argument%D1.8.1 this%D1.6.1 that%D1.6.1
            RAM[16]%D1.6.1 RAM[17]%D1.6.1;

set sp 256,
set local 300,
set argument 400,
set this 3000,
set that 3010,

set RAM[17] 1,   // y = 1
set RAM[16] 0,

repeat 100 { vmstep; }
output;
