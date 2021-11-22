.global _start 

block0:
	SUB	 sp, sp, 256
	STR	 X30, [sp, 240]
	LDR	 X14, [sp, #280]
	STR	 X14, [sp, #24]
	LDR	X2, [sp, #24]
	MOV	X2, X2
	STR	X2, [sp, #104]
	MOV	X3, #8
	STR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	MUL	X4, X2, X3
	STR	X4, [sp, #120]
	LDR	X4, [sp, #120]
	ADD	X4, X4, #0
	LDR	X14, [X13, X4]
	STR	X14, [sp, #128]
	LDR	X5, [sp, #128]
	MOV	X5, X5
	STR	X5, [sp, #32]
	LDR	X6, [sp, #24]
	MOV	X2, X6
	STR	X2, [sp, #104]
	LDR	X2, [sp, #104]
	MOV	X7, X2
	STR	X7, [sp, #40]
block1:
	LDR	X6, [sp, #24]
	MOV	X3, X6
	STR	X3, [sp, #112]
	MOV	X2, #2
	STR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	CMP	X3, X2
	B.LE	l0
	MOV	X3, #0
	B	l1
l0:
	MOV	X3, #1
l1:
	STR	X3, [sp, #112]
	LDR	X3, [sp, #112]
	MOV	X1, #0
	CMP	X1, X3
	B.EQ	block5
block2:
	LDR	X6, [sp, #24]
	MOV	X2, X6
	STR	X2, [sp, #104]
	MOV	X4, #8
	STR	X4, [sp, #120]
	LDR	X2, [sp, #104]
	LDR	X4, [sp, #120]
	MUL	X8, X2, X4
	STR	X8, [sp, #128]
	LDR	X8, [sp, #128]
	ADD	X8, X8, #0
	LDR	X14, [X13, X8]
	STR	X14, [sp, #136]
	LDR	X5, [sp, #32]
	MOV	X2, X5
	STR	X2, [sp, #104]
	LDR	X9, [sp, #136]
	LDR	X2, [sp, #104]
	CMP	X9, X2
	B.LT	l2
	MOV	X3, #0
	B	l3
l2:
	MOV	X3, #1
l3:
	STR	X3, [sp, #112]
	LDR	X3, [sp, #112]
	MOV	X1, #0
	CMP	X1, X3
	B.EQ	block4
block3:
	LDR	X6, [sp, #24]
	MOV	X2, X6
	STR	X2, [sp, #104]
	MOV	X4, #8
	STR	X4, [sp, #120]
	LDR	X2, [sp, #104]
	LDR	X4, [sp, #120]
	MUL	X8, X2, X4
	STR	X8, [sp, #128]
	LDR	X8, [sp, #128]
	ADD	X8, X8, #0
	LDR	X14, [X13, X8]
	STR	X14, [sp, #136]
	LDR	X9, [sp, #136]
	MOV	X5, X9
	STR	X5, [sp, #32]
	LDR	X6, [sp, #24]
	MOV	X2, X6
	STR	X2, [sp, #104]
	LDR	X2, [sp, #104]
	MOV	X7, X2
	STR	X7, [sp, #40]
block4:
	LDR	X6, [sp, #24]
	MOV	X3, X6
	STR	X3, [sp, #112]
	MOV	X2, #1
	STR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	ADD	X3, X3, X2
	STR	X3, [sp, #112]
	LDR	X3, [sp, #112]
	MOV	X6, X3
	STR	X6, [sp, #24]
	B	block1
block5:
	LDR	X7, [sp, #40]
	MOV	X2, X7
	STR	X2, [sp, #104]
	LDR	X2, [sp, #104]
	MOV	 X15, X2
	LDR	 X30, [sp, #240]
	ADD	 sp, sp, #256
	RET
block6:
	LDR	 X30, [sp, #240]
	ADD	 sp, sp, #256
	RET
block7:
	SUB	 sp, sp, 256
	STR	 X30, [sp, 240]
	MOV	X3, #0
	STR	X3, [sp, #112]
	LDR	X3, [sp, #112]
	MOV	X10, X3
	STR	X10, [sp, #48]
block8:
	LDR	X10, [sp, #48]
	MOV	X2, X10
	STR	X2, [sp, #104]
	MOV	X3, #2
	STR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	CMP	X2, X3
	B.LE	l4
	MOV	X2, #0
	B	l5
l4:
	MOV	X2, #1
l5:
	STR	X2, [sp, #104]
	LDR	X2, [sp, #104]
	MOV	X1, #0
	CMP	X1, X2
	B.EQ	block10
block9:
	LDR	X10, [sp, #48]
	MOV	X3, X10
	STR	X3, [sp, #112]
	LDR	X3, [sp, #112]
	STR	X3, [sp, #24]
	BL block0
	MOV	X2, X15
	STR	X2, [sp, #104]
	LDR	X2, [sp, #104]
	MOV	X3, X2
	STR	X3, [sp, #72]
	LDR	X3, [sp, #72]
	MOV	X10, X3
	STR	X10, [sp, #112]
	MOV	X4, #8
	STR	X4, [sp, #120]
	LDR	X3, [sp, #112]
	LDR	X4, [sp, #120]
	MUL	X8, X3, X4
	STR	X8, [sp, #128]
	LDR	X8, [sp, #128]
	ADD	X8, X8, #0
	LDR	X14, [X13, X8]
	STR	X14, [sp, #136]
	LDR	X9, [sp, #136]
	MOV	X5, X9
	STR	X5, [sp, #64]
	LDR	X5, [sp, #48]
	MOV	X2, X5
	STR	X2, [sp, #104]
	MOV	X3, #8
	STR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	MUL	X4, X2, X3
	STR	X4, [sp, #120]
	LDR	X4, [sp, #120]
	ADD	X4, X4, #0
	LDR	X14, [X13, X4]
	STR	X14, [sp, #128]
	LDR	X8, [sp, #128]
	MOV	X7, X8
	STR	X7, [sp, #80]
	LDR	X7, [sp, #80]
	MOV	X2, X7
	STR	X2, [sp, #104]
	LDR	X7, [sp, #72]
	MOV	X3, X7
	STR	X3, [sp, #112]
	MOV	X4, #8
	STR	X4, [sp, #120]
	LDR	X3, [sp, #112]
	LDR	X4, [sp, #120]
	MUL	X8, X3, X4
	STR	X8, [sp, #128]
	LDR	X8, [sp, #128]
	ADD	X8, X8, #0
	STR	X2, [X13, X8]
	LDR	X7, [sp, #64]
	MOV	X9, X7
	STR	X9, [sp, #136]
	LDR	X5, [sp, #48]
	MOV	X2, X5
	STR	X2, [sp, #104]
	MOV	X3, #8
	STR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	MUL	X4, X2, X3
	STR	X4, [sp, #120]
	LDR	X4, [sp, #120]
	ADD	X4, X4, #0
	STR	X7, [X13, X4]
	LDR	X5, [sp, #48]
	MOV	X8, X5
	STR	X8, [sp, #128]
	MOV	X2, #1
	STR	X2, [sp, #104]
	LDR	X5, [sp, #128]
	LDR	X2, [sp, #104]
	ADD	X3, X5, X2
	STR	X3, [sp, #112]
	LDR	X3, [sp, #112]
	MOV	X7, X3
	STR	X7, [sp, #48]
	B	block8
block10:
	LDR	 X30, [sp, #240]
	ADD	 sp, sp, #256
	RET
block11:
	SUB	 sp, sp, 256
	STR	 X30, [sp, 240]
	LDR	 X14, [sp, #344]
	STR	 X14, [sp, #88]
	LDR	 X30, [sp, #240]
	ADD	 sp, sp, #256
	RET
block12:
	SUB	 sp, sp, 256
	STR	 X30, [sp, 240]
	MOV	X2, #0
	STR	X2, [sp, #104]
	LDR	X2, [sp, #104]
	MOV	 X15, X2
	LDR	 X30, [sp, #240]
	ADD	 sp, sp, #256
	RET
block13:
	LDR	 X30, [sp, #240]
	ADD	 sp, sp, #256
	RET
_start:
block14:
	MOV	X13, sp
	MOV	X3, #0
	STR	X3, [sp, #112]
	LDR	X3, [sp, #112]
	MOV	X7, X3
	STR	X7, [sp, #96]
	MOV	X2, #3
	STR	X2, [sp, #104]
	MOV	X3, #0
	STR	X3, [sp, #112]
	MOV	X4, #8
	STR	X4, [sp, #120]
	LDR	X3, [sp, #112]
	LDR	X4, [sp, #120]
	MUL	X5, X3, X4
	STR	X5, [sp, #128]
	LDR	X5, [sp, #128]
	ADD	X5, X5, #0
	STR	X2, [X13, X5]
	MOV	X9, #2
	STR	X9, [sp, #136]
	MOV	X2, #1
	STR	X2, [sp, #104]
	MOV	X3, #8
	STR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	MUL	X4, X2, X3
	STR	X4, [sp, #120]
	LDR	X4, [sp, #120]
	ADD	X4, X4, #0
	STR	X9, [X13, X4]
	MOV	X5, #1
	STR	X5, [sp, #128]
	MOV	X2, #2
	STR	X2, [sp, #104]
	MOV	X3, #8
	STR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	MUL	X4, X2, X3
	STR	X4, [sp, #120]
	LDR	X4, [sp, #120]
	ADD	X4, X4, #0
	STR	X5, [X13, X4]
	BL block7
	MOV	X9, X15
	STR	X9, [sp, #136]
	MOV	X7, #0
	STR	X7, [sp, #144]
	STR	X2, [sp, #104]
	LDR	X7, [sp, #144]
	MOV	X2, X7
	STR	X2, [sp, #96]
block15:
	LDR	X2, [sp, #96]
	MOV	X7, X2
	STR	X7, [sp, #104]
	MOV	X3, #2
	STR	X3, [sp, #112]
	LDR	X2, [sp, #104]
	LDR	X3, [sp, #112]
	CMP	X2, X3
	B.LE	l6
	MOV	X2, #0
	B	l7
l6:
	MOV	X2, #1
l7:
	STR	X2, [sp, #104]
	LDR	X2, [sp, #104]
	MOV	X1, #0
	CMP	X1, X2
	B.EQ	block17
block16:
	STR	X2, [sp, #104]
	LDR	X2, [sp, #96]
	MOV	X3, X2
	STR	X3, [sp, #112]
	MOV	X4, #8
	STR	X4, [sp, #120]
	LDR	X2, [sp, #112]
	LDR	X4, [sp, #120]
	MUL	X5, X2, X4
	STR	X5, [sp, #128]
	LDR	X5, [sp, #128]
	ADD	X5, X5, #0
	LDR	X14, [X13, X5]
	STR	X14, [sp, #136]
	LDR	X9, [sp, #136]
	STR	X9, [sp, #88]
	BL block11
	MOV	X7, X15
	STR	X7, [sp, #104]
	LDR	X9, [sp, #96]
	MOV	X2, X9
	STR	X2, [sp, #112]
	MOV	X7, #1
	STR	X7, [sp, #104]
	LDR	X2, [sp, #112]
	LDR	X7, [sp, #104]
	ADD	X2, X2, X7
	STR	X2, [sp, #112]
	LDR	X2, [sp, #112]
	MOV	X9, X2
	STR	X9, [sp, #96]
	B	block15
block17:
	mov	X0, #0
	mov	X16, #1
	svc	#0x80
