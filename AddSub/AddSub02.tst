// AddSub02.tst — Test (a=10, b=20, x=15) ⇒ x' = (10+20)−15 = 15
load AddSub.vm,
output-file AddSub02.out,
compare-to AddSub02.cmp,
output-list sp%D1.6.1 local%D1.6.1 argument%D1.8.1 this%D1.6.1 that%D1.6.1
            RAM[16]%D1.6.1 RAM[17]%D1.6.1 RAM[18]%D1.6.1
            local[0]%D1.8.1 local[1]%D1.8.1 local[2]%D1.8.1
            argument[0]%D1.11.1 argument[1]%D1.11.1 argument[2]%D1.11.1;

// --- Initialize segments ---
set sp 256,
set local 300,
set argument 400,
set this 3000,
set that 3010,

// --- Initialize statics ---
set RAM[16] 15,   // x = 15
set RAM[17] 2,
set RAM[18] 3,

// --- Initialize locals ---
set local[0] 10,  // a = 10
set local[1] 20,  // b = 20
set local[2] 30,

// --- (Optional) fill arguments ---
set argument[0] 100,
set argument[1] 200,
set argument[2] 300,

// --- Run the VM code ---
repeat 25 { vmstep; }

// --- Output & compare ---
output;
