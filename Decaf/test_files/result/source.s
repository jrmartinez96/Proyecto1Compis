.global _main 

_main:

block0:
	MOV X2, #1
	MOV X15, #8
	STR X2, [X15]
	MOV X15, #8
	LDR X2, [X15]
	MOV X3, X2
	MOV X15, #0
	STR X3, [X15]
	MOV X4, #1
	MOV X15, #16
	STR X4, [X15]
	MOV X15, #16
	LDR X4, [X15]
	MOV X5, X4
	MOV X15, #4
	STR X5, [X15]
block1:
	MOV X15, #0
	LDR X3, [X15]
	MOV X2, X3
	MOV X15, #8
	STR X2, [X15]
	MOV X4, #10
	MOV X15, #16
	STR X4, [X15]
	MOV X15, #8
	LDR X2, [X15]
	MOV X15, #16
	LDR X4, [X15]
	CMP X2, X4
	B.LE l0
	MOV X2, #0
	B l1
l0:
	MOV X2, #1
l1:
	MOV X15, #8
	STR X2, [X15]
	MOV X15, #8
	LDR X2, [X15]
	MOV X1, #0
	CMP X1, X2
	B.EQ block3
block2:
	MOV X15, #0
	LDR X3, [X15]
	MOV X4, X3
	MOV X15, #16
	STR X4, [X15]
	MOV X15, #4
	LDR X5, [X15]
	MOV X2, X5
	MOV X15, #8
	STR X2, [X15]
	MOV X15, #16
	LDR X3, [X15]
	MOV X15, #8
	LDR X2, [X15]
	ADD X3, X3, X2
	MOV X15, #16
	STR X3, [X15]
	MOV X15, #16
	LDR X3, [X15]
	MOV X6, X3
	MOV X15, #0
	STR X6, [X15]
	B block1
block3:
block4:
