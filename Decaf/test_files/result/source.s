.global _start 

block0:
	SUB	 sp, sp, #512
	STR	 X30, [sp, #496]
	STR	 X0, [sp, #0]
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
block1:
	SUB	 sp, sp, #512
	STR	 X30, [sp, #496]
	STR	 X0, [sp, #8]
	LDR	X2, [sp, #8]
	MOV	X2, X2
	STR	X2, [sp, #72]
	MOV	X3, #1
	STR	X3, [sp, #80]
	LDR	X2, [sp, #72]
	LDR	X3, [sp, #80]
	CMP	X2, X3
	B.LE	l0
	MOV	X2, #0
	B	l1
l0:
	MOV	X2, #1
l1:
	STR	X2, [sp, #72]
	LDR	X2, [sp, #72]
	MOV	X1, #0
	CMP	X1, X2
	B.EQ	block4
block2:
	LDR	X4, [sp, #8]
	MOV	X3, X4
	STR	X3, [sp, #80]
	LDR	X3, [sp, #80]
	MOV	 X15, X3
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
block3:
	B	block6
block4:
	LDR	X4, [sp, #8]
	MOV	X2, X4
	STR	X2, [sp, #72]
	MOV	X3, #1
	STR	X3, [sp, #80]
	LDR	X2, [sp, #72]
	LDR	X3, [sp, #80]
	SUB	X2, X2, X3
	STR	X2, [sp, #72]
	LDR	X2, [sp, #72]
	MOV	X5, X2
	STR	X5, [sp, #16]
	LDR	X4, [sp, #8]
	MOV	X3, X4
	STR	X3, [sp, #80]
	MOV	X2, #2
	STR	X2, [sp, #72]
	LDR	X3, [sp, #80]
	LDR	X2, [sp, #72]
	SUB	X3, X3, X2
	STR	X3, [sp, #80]
	LDR	X3, [sp, #80]
	MOV	X6, X3
	STR	X6, [sp, #24]
	LDR	X5, [sp, #16]
	MOV	X2, X5
	STR	X2, [sp, #72]
	LDR	X0, [sp, #72]
	BL block1
	MOV	X3, X15
	STR	X3, [sp, #80]
	LDR	X3, [sp, #80]
	MOV	X7, X3
	STR	X7, [sp, #32]
	LDR	X6, [sp, #24]
	MOV	X2, X6
	STR	X2, [sp, #72]
	LDR	X0, [sp, #72]
	BL block1
	MOV	X3, X15
	STR	X3, [sp, #80]
	LDR	X3, [sp, #80]
	MOV	X8, X3
	STR	X8, [sp, #40]
	LDR	X7, [sp, #32]
	MOV	X2, X7
	STR	X2, [sp, #72]
	LDR	X8, [sp, #40]
	MOV	X3, X8
	STR	X3, [sp, #80]
	LDR	X2, [sp, #72]
	LDR	X3, [sp, #80]
	ADD	X2, X2, X3
	STR	X2, [sp, #72]
	LDR	X2, [sp, #72]
	MOV	X9, X2
	STR	X9, [sp, #48]
	LDR	X9, [sp, #48]
	MOV	X3, X9
	STR	X3, [sp, #80]
	LDR	X3, [sp, #80]
	MOV	 X15, X3
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
block5:
block6:
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
_start:
block7:
	MOV	X13, sp
	MOV	X2, #9
	STR	X2, [sp, #72]
	LDR	X2, [sp, #72]
	MOV	X10, X2
	STR	X10, [sp, #56]
	LDR	X10, [sp, #56]
	MOV	X3, X10
	STR	X3, [sp, #80]
	LDR	X0, [sp, #80]
	BL block1
	MOV	X2, X15
	STR	X2, [sp, #72]
	LDR	X2, [sp, #72]
	MOV	X5, X2
	STR	X5, [sp, #64]
	LDR	X5, [sp, #64]
	MOV	X3, X5
	STR	X3, [sp, #80]
	LDR	X0, [sp, #80]
	BL block0
	MOV	X2, X15
	STR	X2, [sp, #72]
	mov	X0, #0
	mov	X16, #1
	svc	#0x80
