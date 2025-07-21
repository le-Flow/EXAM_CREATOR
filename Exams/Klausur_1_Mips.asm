1.
	Quatschie Aufgabe
2.

addi $t0, $zero, 0
Loop1:
	slt $t4, $t0, $s0
	beq $t4, $zero, end
	addi $t1, $zero, 0
	Loop2:	
		slt $t4, $t1, $s1
		beq $t4, $zero, end2
		sll $t2, $t1, 4
		add $t2, $t2, $s2
		add $t3, $t0, $t1
		sw $t3, 0[$t2]
		addi $t1, $t1, 1
		j Loop2
	end2:	
		addi $t0, $t0, 1
		j Loop1