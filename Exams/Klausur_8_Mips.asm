.data

# a = $s0
# b = $s1
# D = $s2
# i = $t0
# j = $t1

.text
addi $t0, $zero, -1
outer_loop:
    addi $t1, $zero, 0 # j = 0
    addi $t0, $t0, 1 # i++
    slt $t2, $t0, $s0
    beq $t2, $zero, end
    inner_loop:
        slt $t3, $t1, $s1
        beq $t3, $zero, outer_loop
        sll $t4, $t2, 2 # j*4
        addi $t4, $t4, $s2 # *D[4*j]
        addi $t5, $t0, $t1
        sw $t5, 0($t4)
        addi $t1, $t1, 1 # j++
        j inner_loop

end: