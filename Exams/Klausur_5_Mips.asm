Kette aus Ascii Ziffern (+ und - ganzzahlen)
soll als ganzzahlen in $a0 gespeichert werden


string_to_int:
    li $v0, 0
    addi $sp, $sp, -4
    sw $a0, 0($sp)
    li $t3, 10
    Loop:
        lb $t0, 0($a0)
        beq $t0, $zero, end
        addi $t0, $t0, -'0' # ASCI Basis entfernen
        slti t1, t0, 10
        beq $t1, $zero, NaN
        mul $v0, $v0, $t3
        add $v0, $v0, $t0
        addi $a0, $a0, 1
        j Loop

NaN:
    addi $v0, $zero, -1
    lw $a0, 0($sp)
    addi $sp, $sp, 4
    jr $ra
end:
    lw $a0, 0($sp)
    addi $sp, $sp, 4
    jr $ra