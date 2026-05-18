bits 64

		section .text

        global _start

_start:

    	mov rax, 1
		mov rcx, 1
    	mov rdi , rax
    	mov rax , 60 ; exit
    	syscall
