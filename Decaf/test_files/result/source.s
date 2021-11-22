.global _main 

block0:
	STR	 X30, [sp, 496]
	ADD	 sp, sp, 512
	LDR	X2, [sp, #24]
	MOV	X2, X2
	STR	X2, [sp, #32]
	LDR	 X14, [sp, #0]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #0]
	ADD	 sp, sp, #512
	LDR	 X14, [sp, #8]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #8]
	ADD	 sp, sp, #512
	LDR	 X14, [sp, #16]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #16]
	ADD	 sp, sp, #512
	LDR	X2, [sp, #32]
	MOV	 X15, X2
	SUB	 sp, sp, #512
	LDR	 X30, [sp, #496]
	RET
block1:
	LDR	 X14, [sp, #0]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #0]
	ADD	 sp, sp, #512
	LDR	 X14, [sp, #8]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #8]
	ADD	 sp, sp, #512
	LDR	 X14, [sp, #16]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #16]
	ADD	 sp, sp, #512
	SUB	 sp, sp, #512
	LDR	 X30, [sp, #496]
	RET
_main:
block2:
	STR	 X30, [sp, 496]
	ADD	 sp, sp, 512
	MOV	X3, #5
	STR	X3, [sp, #40]
	MOV	X2, #0
	STR	X2, [sp, #32]
	MOV	X3, #0
	STR	X3, [sp, #40]
	LDR	X2, [sp, #32]
	LDR	X3, [sp, #40]
	MUL	X4, X2, X3
	STR	X4, [sp, #48]
	LDR	X4, [sp, #48]
	ADD	X4, X4, #0
	STR	X3, [sp, X4]
	MOV	X5, #6
	STR	X5, [sp, #56]
	MOV	X2, #1
	STR	X2, [sp, #32]
	MOV	X3, #0
	STR	X3, [sp, #40]
	LDR	X2, [sp, #32]
	LDR	X3, [sp, #40]
	MUL	X4, X2, X3
	STR	X4, [sp, #48]
	LDR	X4, [sp, #48]
	ADD	X4, X4, #0
	STR	X5, [sp, X4]
	MOV	X5, #7
	STR	X5, [sp, #56]
	MOV	X2, #3
	STR	X2, [sp, #32]
	MOV	X3, #0
	STR	X3, [sp, #40]
	LDR	X2, [sp, #32]
	LDR	X3, [sp, #40]
	MUL	X4, X2, X3
	STR	X4, [sp, #48]
	LDR	X4, [sp, #48]
	ADD	X4, X4, #0
	STR	X5, [sp, X4]
	MOV	X5, #3
	STR	X5, [sp, #56]
	MOV	X2, #0
	STR	X2, [sp, #32]
	LDR	X5, [sp, #56]
	LDR	X2, [sp, #32]
	MUL	X3, X5, X2
	STR	X3, [sp, #40]
	LDR	X3, [sp, #40]
	ADD	X3, X3, #0
	LDR	X14, [sp, X3]
	STR	X14, [sp, #48]
	LDR	X4, [sp, #48]
	STR	X4, [sp, #24]
	LDR	 X14, [sp, #0]
	ADD	 sp, sp, #512
	STR	 X14, [sp, #0]
	SUB	 sp, sp, #512
	LDR	 X14, [sp, #8]
	ADD	 sp, sp, #512
	STR	 X14, [sp, #8]
	SUB	 sp, sp, #512
	LDR	 X14, [sp, #16]
	ADD	 sp, sp, #512
	STR	 X14, [sp, #16]
	SUB	 sp, sp, #512
	LDR	 X14, [sp, #24]
	ADD	 sp, sp, #512
	STR	 X14, [sp, #24]
	SUB	 sp, sp, #512
	BL block0
	MOV	X2, X15
	STR	X2, [sp, #32]
	LDR	 X14, [sp, #0]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #0]
	ADD	 sp, sp, #512
	LDR	 X14, [sp, #8]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #8]
	ADD	 sp, sp, #512
	LDR	 X14, [sp, #16]
	SUB	 sp, sp, #512
	STR	 X14, [sp, #16]
	ADD	 sp, sp, #512
	SUB	 sp, sp, #512
	LDR	 X30, [sp, #496]
	RET
	mov	X0, #0
	mov	X16, #1
	svc	#0x80
