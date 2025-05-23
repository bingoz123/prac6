// Mult01.tst — Test (x = 4, y = 6) ⇒ a = 24
load Mult.vm,
output-file Mult01.out,
compare-to Mult01.cmp,
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
set RAM[16] 4,    // x = 4
set RAM[17] 6,    // y = 6
set RAM[18] 0,    // unused

// --- Initialize locals (a and counter) ---
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
