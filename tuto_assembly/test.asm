extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a : dq 0
   global main
    section .text
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
                    push rax
                    mov rax, 0x0A22646E6569724620794D206F6C6C654822  
                    push rax
                    mov rdi, rsp
                    mov rsi, rax
                    xor rax, rax
                    call printf
                    add rsp, 16
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            