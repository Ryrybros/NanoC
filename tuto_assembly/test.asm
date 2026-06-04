extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a : dq 0
t : dq 0
   global main
    section .text
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
            
    mov rax, 8
    mov rdi, rax
    call malloc
            mov [t] , rax
            
                   
    mov rax, [t]     

            push rax
            
    mov rax, 8
    mov rdi, rax
    call malloc
            pop rbx
            mov [rbx] , rax
            
                   
    mov rax, [t]     
    mov rax, [rax]

            push rax
            
    mov rax, 8
    mov rdi, rax
    call malloc
            pop rbx
            mov [rbx] , rax
            
                    
     
            mov rax, 0
            push rax
                    
     
            mov rax, 0
            push rax
            mov rax, [t]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            mov [a] , rax
            
                    mov rdi, asm_int_prtr
                    mov rsi, [a]
                    xor rax, rax
                    call printf
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            