// Fib01.tst — Test Fib.fib(0) ⇒ 0
load Fib.vm,
output-file Fib01.out,
compare-to Fib01.cmp,
output-list sp%D1.6.1 local%D1.6.1 argument%D1.8.1 this%D1.6.1 that%D1.6.1
            RAM[16]%D1.6.1 RAM[17]%D1.6.1;

// initialize segments
set sp 256,
set local 300,
set argument 400,
set this 3000,
set that 3010,

// test input
set RAM[17] 0,   // y = 0
set RAM[16] 0,   // clear x

// run bootstrap + Fib.fib
repeat 100 { vmstep; }

// compare
output;
