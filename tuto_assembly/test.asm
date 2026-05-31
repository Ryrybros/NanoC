extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a: dq 0 
   global main
    section .text
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            mov qword [a] , 2

                         
        mov rax, 1
        push rax
        mov rax, [a]
        pop rbx
        add rax, rbx
        
    
                        mov qword [a] , rax
                
                    mov rdi, asm_int_prtr
                    mov rsi, [a]
                    xor rax, rax
                    call printf
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            