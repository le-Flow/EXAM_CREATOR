addi $v0, $0, $0
Fib:
	beq $a0, $0, zerocase
	li $t1, 1
	beq $a0, $t1, onecase
	addi $sp, $sp, -8
	sw $ra, 4($sp)
	sw $a0, 0($sp)
	addi $a0, $a0, -1
	jal Fib
	lw $a0, 0($sp)
	addi $a0, $a0, -2
	jal Fib
	lw $ra, 4($sp)
	addi $sp, $sp, 8
	jr $ra
zerocase:
	jr $ra
onecase:
	add $v0, $v0, 1
	jr $ra