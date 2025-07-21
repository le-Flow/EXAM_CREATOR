addi R5, $0, $0 # i = 0
Loop:
	beq R5, R6, end
	sll R12, R5, 2
	add R11, R1, R12
	lw R10, 0(R11)
	lw R11, 4(R11)
	sub R10, R10, R11
	
	add R12, R2, R12
	sw R10, 0(R12)
	
	addi R5, R5, 2
	j Loop
end: