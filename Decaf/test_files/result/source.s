.global _start 

block0:
	SUB	 sp, sp, #512
	STR	 X30, [sp, #496]
	STR	 X0, [sp, #80]
	LDR	X2, [sp, #80]
	MOV	X2, X2
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	LDR	X14, [X13, X4]
	STR	X14, [sp, #184]
	LDR	X5, [sp, #184]
	MOV	X5, X5
	STR	X5, [sp, #88]
	LDR	X6, [sp, #80]
	MOV	X2, X6
	STR	X2, [sp, #160]
	LDR	X2, [sp, #160]
	MOV	X7, X2
	STR	X7, [sp, #96]
block1:
	LDR	X6, [sp, #80]
	MOV	X3, X6
	STR	X3, [sp, #168]
	MOV	X2, #10
	STR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	CMP	X3, X2
	B.LT	l0
	MOV	X3, #0
	B	l1
l0:
	MOV	X3, #1
l1:
	STR	X3, [sp, #168]
	LDR	X3, [sp, #168]
	MOV	X1, #0
	CMP	X1, X3
	B.EQ	block5
block2:
	LDR	X6, [sp, #80]
	MOV	X2, X6
	STR	X2, [sp, #160]
	MOV	X4, #8
	STR	X4, [sp, #176]
	LDR	X2, [sp, #160]
	LDR	X4, [sp, #176]
	MUL	X8, X2, X4
	STR	X8, [sp, #184]
	LDR	X8, [sp, #184]
	ADD	X8, X8, #0
	LDR	X14, [X13, X8]
	STR	X14, [sp, #192]
	LDR	X5, [sp, #88]
	MOV	X2, X5
	STR	X2, [sp, #160]
	LDR	X9, [sp, #192]
	LDR	X2, [sp, #160]
	CMP	X9, X2
	B.LT	l2
	MOV	X3, #0
	B	l3
l2:
	MOV	X3, #1
l3:
	STR	X3, [sp, #168]
	LDR	X3, [sp, #168]
	MOV	X1, #0
	CMP	X1, X3
	B.EQ	block4
block3:
	LDR	X6, [sp, #80]
	MOV	X2, X6
	STR	X2, [sp, #160]
	MOV	X4, #8
	STR	X4, [sp, #176]
	LDR	X2, [sp, #160]
	LDR	X4, [sp, #176]
	MUL	X8, X2, X4
	STR	X8, [sp, #184]
	LDR	X8, [sp, #184]
	ADD	X8, X8, #0
	LDR	X14, [X13, X8]
	STR	X14, [sp, #192]
	LDR	X9, [sp, #192]
	MOV	X5, X9
	STR	X5, [sp, #88]
	LDR	X6, [sp, #80]
	MOV	X2, X6
	STR	X2, [sp, #160]
	LDR	X2, [sp, #160]
	MOV	X7, X2
	STR	X7, [sp, #96]
block4:
	LDR	X6, [sp, #80]
	MOV	X3, X6
	STR	X3, [sp, #168]
	MOV	X2, #1
	STR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	ADD	X3, X3, X2
	STR	X3, [sp, #168]
	LDR	X3, [sp, #168]
	MOV	X6, X3
	STR	X6, [sp, #80]
	B	block1
block5:
	LDR	X7, [sp, #96]
	MOV	X2, X7
	STR	X2, [sp, #160]
	LDR	X2, [sp, #160]
	MOV	 X15, X2
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
block6:
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
block7:
	SUB	 sp, sp, #512
	STR	 X30, [sp, #496]
	MOV	X3, #0
	STR	X3, [sp, #168]
	LDR	X3, [sp, #168]
	MOV	X10, X3
	STR	X10, [sp, #104]
block8:
	LDR	X10, [sp, #104]
	MOV	X2, X10
	STR	X2, [sp, #160]
	MOV	X3, #10
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	CMP	X2, X3
	B.LT	l4
	MOV	X2, #0
	B	l5
l4:
	MOV	X2, #1
l5:
	STR	X2, [sp, #160]
	LDR	X2, [sp, #160]
	MOV	X1, #0
	CMP	X1, X2
	B.EQ	block10
block9:
	LDR	X10, [sp, #104]
	MOV	X3, X10
	STR	X3, [sp, #168]
	LDR	X0, [sp, #168]
	BL block0
	MOV	X2, X15
	STR	X2, [sp, #160]
	LDR	X2, [sp, #160]
	MOV	X5, X2
	STR	X5, [sp, #128]
	LDR	X5, [sp, #128]
	MOV	X3, X5
	STR	X3, [sp, #168]
	MOV	X4, #8
	STR	X4, [sp, #176]
	LDR	X3, [sp, #168]
	LDR	X4, [sp, #176]
	MUL	X8, X3, X4
	STR	X8, [sp, #184]
	LDR	X8, [sp, #184]
	ADD	X8, X8, #0
	LDR	X14, [X13, X8]
	STR	X14, [sp, #192]
	LDR	X9, [sp, #192]
	MOV	X5, X9
	STR	X5, [sp, #120]
	LDR	X10, [sp, #104]
	MOV	X2, X10
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	LDR	X14, [X13, X4]
	STR	X14, [sp, #184]
	LDR	X8, [sp, #184]
	MOV	X5, X8
	STR	X5, [sp, #136]
	LDR	X5, [sp, #136]
	MOV	X2, X5
	STR	X2, [sp, #160]
	LDR	X9, [sp, #128]
	MOV	X3, X9
	STR	X3, [sp, #168]
	MOV	X4, #8
	STR	X4, [sp, #176]
	LDR	X3, [sp, #168]
	LDR	X4, [sp, #176]
	MUL	X8, X3, X4
	STR	X8, [sp, #184]
	LDR	X8, [sp, #184]
	ADD	X8, X8, #0
	STR	X2, [X13, X8]
	LDR	X5, [sp, #120]
	MOV	X5, X5
	STR	X5, [sp, #192]
	LDR	X10, [sp, #104]
	MOV	X2, X10
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X5, [X13, X4]
	LDR	X10, [sp, #104]
	MOV	X8, X10
	STR	X8, [sp, #184]
	MOV	X2, #1
	STR	X2, [sp, #160]
	LDR	X8, [sp, #184]
	LDR	X2, [sp, #160]
	ADD	X3, X8, X2
	STR	X3, [sp, #168]
	LDR	X3, [sp, #168]
	MOV	X10, X3
	STR	X10, [sp, #104]
	B	block8
block10:
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
block11:
	SUB	 sp, sp, #512
	STR	 X30, [sp, #496]
	STR	 X0, [sp, #144]
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
block12:
	SUB	 sp, sp, #512
	STR	 X30, [sp, #496]
	MOV	X2, #0
	STR	X2, [sp, #160]
	LDR	X2, [sp, #160]
	MOV	 X15, X2
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
block13:
	LDR	 X30, [sp, #496]
	ADD	 sp, sp, #512
	RET
_start:
block14:
	MOV	X13, sp
	MOV	X3, #3
	STR	X3, [sp, #168]
	MOV	X2, #0
	STR	X2, [sp, #160]
	MOV	X4, #8
	STR	X4, [sp, #176]
	LDR	X2, [sp, #160]
	LDR	X4, [sp, #176]
	MUL	X8, X2, X4
	STR	X8, [sp, #184]
	LDR	X8, [sp, #184]
	ADD	X8, X8, #0
	STR	X3, [X13, X8]
	MOV	X5, #1
	STR	X5, [sp, #192]
	MOV	X2, #1
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X5, [X13, X4]
	MOV	X8, #2
	STR	X8, [sp, #184]
	MOV	X2, #2
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X8, [X13, X4]
	MOV	X5, #6
	STR	X5, [sp, #192]
	MOV	X2, #3
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X5, [X13, X4]
	MOV	X8, #7
	STR	X8, [sp, #184]
	MOV	X2, #4
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X8, [X13, X4]
	MOV	X5, #5
	STR	X5, [sp, #192]
	MOV	X2, #5
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X5, [X13, X4]
	MOV	X8, #10
	STR	X8, [sp, #184]
	MOV	X2, #6
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X8, [X13, X4]
	MOV	X5, #9
	STR	X5, [sp, #192]
	MOV	X2, #7
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X5, [X13, X4]
	MOV	X8, #4
	STR	X8, [sp, #184]
	MOV	X2, #8
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X8, [X13, X4]
	MOV	X5, #8
	STR	X5, [sp, #192]
	MOV	X2, #9
	STR	X2, [sp, #160]
	MOV	X3, #8
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	MUL	X4, X2, X3
	STR	X4, [sp, #176]
	LDR	X4, [sp, #176]
	ADD	X4, X4, #0
	STR	X5, [X13, X4]
	BL block7
	MOV	X8, X15
	STR	X8, [sp, #184]
	MOV	X6, #0
	STR	X6, [sp, #200]
	LDR	X6, [sp, #200]
	MOV	X7, X6
	STR	X7, [sp, #152]
block15:
	LDR	X7, [sp, #152]
	MOV	X2, X7
	STR	X2, [sp, #160]
	MOV	X3, #10
	STR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	CMP	X2, X3
	B.LT	l6
	MOV	X2, #0
	B	l7
l6:
	MOV	X2, #1
l7:
	STR	X2, [sp, #160]
	LDR	X2, [sp, #160]
	MOV	X1, #0
	CMP	X1, X2
	B.EQ	block17
block16:
	LDR	X7, [sp, #152]
	MOV	X3, X7
	STR	X3, [sp, #168]
	MOV	X4, #8
	STR	X4, [sp, #176]
	LDR	X3, [sp, #168]
	LDR	X4, [sp, #176]
	MUL	X8, X3, X4
	STR	X8, [sp, #184]
	LDR	X8, [sp, #184]
	ADD	X8, X8, #0
	LDR	X14, [X13, X8]
	STR	X14, [sp, #192]
	LDR	X0, [sp, #192]
	BL block11
	MOV	X2, X15
	STR	X2, [sp, #160]
	LDR	X7, [sp, #152]
	MOV	X3, X7
	STR	X3, [sp, #168]
	MOV	X2, #1
	STR	X2, [sp, #160]
	LDR	X3, [sp, #168]
	LDR	X2, [sp, #160]
	ADD	X3, X3, X2
	STR	X3, [sp, #168]
	LDR	X3, [sp, #168]
	MOV	X7, X3
	STR	X7, [sp, #152]
	B	block15
block17:
	mov	X0, #0
	mov	X16, #1
	svc	#0x80
