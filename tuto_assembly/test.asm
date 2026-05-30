extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    p : dq 0
a : dq 8
endl : db " ",10," ", 0
   global main
    section .text
            ;This is a function
            fib:                    ;Name of func

            push rbp
            mov rbp, rsp
            
            
                    
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
        
    
        mov rsp, rbp           
        pop rbp     
        ret
        
        end_else_0:
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
                     
        mov rax, 2
        push rax
        
         
        mov rax, 1
        push rax
        ;This is a function call
mov rax, [a]
            push rdi
            mov rdi , rax
            mov rax, 0
            push rsi
            mov rsi , rax
            

call fib;end_func_call

            pop rdi
            
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
            