// Abs01.tst — Test (x = 7) ⇒ y = |7| = 7
load Abs.vm,
output-file Abs01.out,
compare-to Abs01.cmp,
output-list sp%D1.6.1 local%D1.6.1 argument%D1.8.1 this%D1.6.1 that%D1.6.1
            RAM[16]%D1.6.1 RAM[17]%D1.6.1 RAM[18]%D1.6.1
            local[0]%D1.8.1 local[1]%D1.8.1 local[2]%D1.8.1
            argument[0]%D1.11.1 argument[1]%D1.11.1 argument[2]%D1.11.1;

// --- initialize segment pointers ---
set sp 256,
set local 300,
set argument 400,
set this 3000,
set that 3010,

// --- initialize static inputs ---
set RAM[16] 7,     // x = 7
set RAM[17] 0,     // y = 0 (initial)
set RAM[18] 0,     // unused

// --- clear other segments (optional) ---
set local[0] 0, set local[1] 0, set local[2] 0,
set argument[0] 0, set argument[1] 0, set argument[2] 0,

// --- run the VM code ---
repeat 20 { vmstep; }

// --- output & compare ---
output;
