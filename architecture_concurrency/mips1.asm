	.data
vals:    .word 4, 5, 8, 0
	.space 16
	.word 4: 0xbfff
	.text

	.globl main

main:
	addi $a0, $0, 24 # malloc 24 bytes
	li $v0, 9
	syscall
	
	
	li $v0, 10	

	syscall	