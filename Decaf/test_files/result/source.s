.global _main 

_main:
block0:
	LDR	X2, [sp, #40]
	MOV	X2, X2
	STR	X2, [sp, #76]
	MOV	X3, #0
	STR	X3, [sp, #84]
	LDR	X2, [sp, X3]
	LDR	X3, [sp, #84]
	MUL	X4, X2, X3
	STR	X4, [sp, #92]
	LDR	X5, [sp, #100]
	MOV	X5, X5
	STR	X5, [sp, #44]
	LDR	X6, [sp, #40]
	MOV	X2, X6
	STR	X2, [sp, #76]
	LDR	X2, [sp, #76]
	MOV	X7, X2
	STR	X7, [sp, #48]
	mov	X0, #0
	mov	X16, #1
	svc	#0x80
