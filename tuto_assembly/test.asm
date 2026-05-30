extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
<<<<<<< Updated upstream
    p : dq 0
a : dq 8
=======
    x : dq 10
>>>>>>> Stashed changes
endl : db " ",10," ", 0
   global main
    section .text
            ;This is a function
<<<<<<< Updated upstream
            fib:                    ;Name of func
=======
            hallo:                    ;Name of func
>>>>>>> Stashed changes

            push rbp
            mov rbp, rsp
            
<<<<<<< Updated upstream
            
                    
                    push rdi
                    push rsi
                    push rax
                    xor rax, rax
                    mov rdi, asm_int_prtr
                    mov rsi, rsi
                    call printf
                    pop rax
                    pop rsi
                    pop rdi
                    
         
        mov rax, 2
        push rax
        mov rax, rdi
        pop rbx
        cmp rax, rbx
        setl al
        movzx rax, al
    
        cmp rax, 0
        jz end_0
        
        mov rax, 1
        mov rsp, rbp           
        pop rbp     
        ret
        
        jmp end_else_0
        end_0:
        
         
        ;This is a function call
 
        mov rax, 1
        push rax
        mov rax, rdi
        pop rbx
        sub rax, rbx
        
    
            push rdi
            mov rdi , rax
             
        mov rax, 1
        push rax
        mov rax, rsi
        pop rbx
        add rax, rbx
        
    
            push rsi
            mov rsi , rax
            

call fib;end_func_call

            pop rdi
            
            pop rsi
            
        push rax
        ;This is a function call
 
        mov rax, 2
        push rax
        mov rax, rdi
        pop rbx
        sub rax, rbx
        
    
            push rdi
            mov rdi , rax
             
        mov rax, 1
        push rax
        mov rax, rsi
        pop rbx
        add rax, rbx
        
    
            push rsi
            mov rsi , rax
            

call fib;end_func_call

            pop rdi
            
            pop rsi
            
        pop rbx
        add rax, rbx
=======
            mov rdi , 0

         
        mov rax, [x]
        push rax
        mov rax, [x]
        pop rbx
        imul  rax, rbx
>>>>>>> Stashed changes
        
    
        mov rsp, rbp           
        pop rbp     
        ret
<<<<<<< Updated upstream
        
        end_else_0:
=======
>>>>>>> Stashed changes
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
<<<<<<< Updated upstream
                     
        mov rax, 2
        push rax
        
         
        mov rax, 1
        push rax
        ;This is a function call
mov rax, [a]
=======
                    mov rdi, endl
                    xor rax, rax
                    call printf
                ;This is a function call
mov rax, 0
>>>>>>> Stashed changes
            push rdi
            mov rdi , rax
            mov rax, 0
            push rsi
            mov rsi , rax
            

call hallo;end_func_call

            pop rdi
            
<<<<<<< Updated upstream
            pop rsi
            
        pop rbx
        add rax, rbx
        
    
        
        pop rbx
        imul  rax, rbx
        
    
                    mov qword [a] , rax
            
                    mov rdi, endl
                    xor rax, rax
                    call printf
                
                    mov rdi, asm_int_prtr
                    mov rsi, [a]
=======
                    mov rdi, asm_int_prtr
                    mov rsi, rax
>>>>>>> Stashed changes
                    xor rax, rax
                    call printf
                
                    mov rdi, endl
                    xor rax, rax
                    call printf
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            