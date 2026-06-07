extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    p : dq 0
a : dq 0
   global main
    section .text
            ;This is a function
            f:                    ;Name of func

            push rbp
            mov rbp, rsp
            
            
                
    mov rax, rdi     
      
    mov rax, [rax]
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
            mov rax, 4
            mov [a] , rax
            
            mov rax, QWORD a
            mov [p] , rax
            ;This is a function call
mov rax, [p]
                push rdi
                mov rdi , rax
                

call f;end_func_call

                pop rdi
                
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            