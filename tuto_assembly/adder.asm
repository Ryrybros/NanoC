bits 64

		section .text

        global _start

_start:

    mov eax , 10
    mov ebx , 100
    add eax, ebx
    mov rdi , rax
    mov rax , 60 ; exit
    syscall
