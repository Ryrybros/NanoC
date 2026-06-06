extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a : dq 0
t : dq 0
b times 2 dq 0
c times 1 dq 0
   global main
    section .text
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi

            mov rax, b
            mov [b], rax
mov rax, c
            mov [c], rax


            
            
            
    mov rax, 8
    mov rdi, rax
    call malloc
            mov [t] , rax
            
                   
     
            mov rax, 1
            push rax
            mov rax, [t]
            pop rbx
            add rax, rbx
            
             

            push rax
            mov rax, 506978305677
            pop rbx
            mov [rbx] , rax
            
                    
     
            mov rax, 1
            push rax
            mov rax, [t]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            mov [a] , rax
            
                   
     
            mov rax, 1
            push rax
            mov rax, [b]
            pop rbx
            add rax, rbx
            
             

            push rax
            mov rax, 25
            pop rbx
            mov [rbx] , rax
            
                    
     
            mov rax, 1
            push rax
            mov rax, [b]
            pop rbx
            add rax, rbx
            
             
      
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
            