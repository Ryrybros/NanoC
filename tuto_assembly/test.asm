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
            
            
                    
                    

                    mov rax, 0x00
                    push rax

                    mov rax, 0x0A
                    push rax
                    

                    

                    mov rax, 0x0000003F20756F79
                    push rax 

                    

                    mov rax, 0x2065726120776F68
                    push rax 

                    

                    mov rax, 0x202C646E69726620
                    push rax 

                    

                    mov rax, 0x796D206F6C6C6548
                    push rax 

                    


                    mov rdi, rsp
                    xor rax, rax
                    call printf
                    add rsp, 40
                
                    mov rdi, asm_int_prtr
                    mov rsi, [a]
                    xor rax, rax
                    call printf
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            