// Mult02.tst — Test (x = 7, y = 2) ⇒ a = 14
load Mult.vm,
output-file Mult02.out,
compare-to Mult02.cmp,
output-list sp%D1.6.1 local%D1.6.1 argument%D1.8.1 this%D1.6.1 that%D1.6.1
            RAM[16]%D1.6.1 RAM[17]%D1.6.1 RAM[18]%D1.6.1
            local[0]%D1.8.1 local[1]%D1.8.1 local[2]%D1.8.1
            argument[0]%D1.11.1 argument[1]%D1.11.1 argument[2]%D1.11.1;

// --- Initialize segment pointers ---
set sp 256,
set local 300,
set argument 400,
set this 3000,
set that 3010,

// --- Initialize static inputs ---
set RAM[16] 7,    // x = 7
set RAM[17] 2,    // y = 2
set RAM[18] 0,    // unused

// --- Initialize locals ---
set local[0] 0,   // a = 0
set local[1] 0,   // counter (will be overwritten)
set local[2] 0,   // unused

// --- (Optional) initialize arguments ---
set argument[0] 100,
set argument[1] 200,
set argument[2] 300,

// --- Run your VM code ---
repeat 100 { vmstep; }

// --- Output & compare ---
output;
