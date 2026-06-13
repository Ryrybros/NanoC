extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    t : dq 0
asm_static_tab_p times 5 dq 0
            p : dq 0
a : dq 0
   global main
    section .text
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi

            mov rax, asm_static_tab_p
            mov [p], rax


            
            
            
    mov rax, 8
    
            push rdi ; saving rdi
            
            push rsi ; saving rsi
            
            push rdx ; saving rdx
            
            push rcx ; saving rcx
            
            push r8 ; saving r8
            
            push r9 ; saving r9
            
    mov rdi, rax
    call malloc
    
            pop r9
            
            pop r8
            
            pop rcx
            
            pop rdx
            
            pop rsi
            
            pop rdi
            
    
            mov [t] , rax
            
                   
     
             
            mov rax, 1
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, [t]
            pop rbx
            add rax, rbx
            
             

            push rax
            mov rax, 50
            pop rbx
            mov [rbx] , rax
            
                   
     
             
            mov rax, 1
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, [p]
            pop rbx
            add rax, rbx
            
             

            push rax
            mov rax, [t]
            pop rbx
            mov [rbx] , rax
            
                   
     
             
            mov rax, 2
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
                    
     
             
            mov rax, 1
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, [p]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            add rax, rbx
            
             

            push rax
            mov rax, 15
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 5
            push rax
                    
     
             
            mov rax, 2
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
                    
     
             
            mov rax, 1
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, [p]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            add rax, rbx
            
        
            mov [a] , rax
            
                    mov rbx, [a]
                    
            push rdi ; saving rdi
            
            push rsi ; saving rsi
            
            push rdx ; saving rdx
            
            push rcx ; saving rcx
            
            push r8 ; saving r8
            
            push r9 ; saving r9
            
                    push rax
                    mov rdi, asm_int_prtr
                    mov rsi, rbx
                    xor rax, rax
                    call printf
                    pop rax

                    
            pop r9
            
            pop r8
            
            pop rcx
            
            pop rdx
            
            pop rsi
            
            pop rdi
            
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            