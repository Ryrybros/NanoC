extern printf; e.g stdio.h
section .data
hello: db "h" , "e" , "l", 0x20 , "lo %d" , 10 , 0
prog_info : db "program args :",  "%s" , 10
res: db "%d"
X: dq 10
global main

section .text
main:
    push rbp
    mov rbp , rsp 
    mov [X], 1
    mov rbx, [X]

    xor rcx , rcx
    
    loop:
        inc rcx
        imul rbx, rcx
        cmp rcx, 5
        jne loop
    
    mov rax, 0
    mov rdi, res
    mov rax , 10
    cmp rax , 15
    setl al
    movzx rax, al
    cmp rax, 0
    mov rsi ,rbx
    je end
    call printf
    end:
    pop rbp
    ret