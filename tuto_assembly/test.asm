extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a: dq 0 
b: dq 0 
c: dq 0 
   global main
    section .text
            ;This is a function
            hello:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    
                    sub rsp, 16
                mov qword [rbp - 8],a

            
                     
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
                
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
                    mov rax, 4
                    mov qword [a] , rax
                       
    mov rax, QWORD a
    mov [b], rax

                            
    mov rax, [b]     
      
    mov rax, [rax]
                    mov qword [c] , rax
                
                    mov rdi, asm_int_prtr
                    mov rsi, [c]
                    xor rax, rax
                    call printf
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            