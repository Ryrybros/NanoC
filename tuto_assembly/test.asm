extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    a : dq 8
endl : db " ",10," ", 0
e: dq 0 
   global main
    section .text
            ;This is a function
            fib:                    ;Name of func

            push rbp
            mov rbp, rsp
            
            
         
        mov rax, 2
        push rax
        mov rax, rdi
        pop rbx
        cmp rax, rbx
        setl al
        movzx rax, al
    
        cmp rax, 0
        jz end
        
        mov rax, 1
        mov rsp, rbp           
        pop rbp     
        ret
        
        jmp end_else
        end:
        
         
        ;This is a function call
 
        mov rax, 1
        push rax
        mov rax, rdi
        pop rbx
        sub rax, rbx
        
    
            push rdi
            mov rdi , rax
            

call fib;end_func_call

            pop rdi
            
        push rax
        ;This is a function call
 
        mov rax, 2
        push rax
        mov rax, rdi
        pop rbx
        sub rax, rbx
        
    
            push rdi
            mov rdi , rax
            

call fib;end_func_call

            pop rdi
            
        pop rbx
        add rax, rbx
        
    
        mov rsp, rbp           
        pop rbp     
        ret
        
        end_else:
            
            
        main:
        push rbp            
        mov rbp, rsp
        mov [argv], rsi
        
        
            ;This is a function call
mov rax, [a]
            push rdi
            mov rdi , rax
            

call fib;end_func_call

            pop rdi
            
            mov qword [a] , rax
            
                    mov rdi, endl
                    call printf
                
                    mov rdi, asm_int_prtr
                    mov rsi, [a] 
                    call printf
                
                    mov rdi, endl
                    xor rax, rax
                    call printf
                
                     
        mov rax, 10
        push rax
         
        mov rax, [a]
        push rax
        mov rax, [e]
        pop rbx
        add rax, rbx
        
    
        pop rbx
        add rax, rbx
        
    
                    mov qword [e] , rax
            
                    mov rdi, asm_int_prtr
                    mov rsi, [e] 
                    call printf
                
                    mov rdi, endl
                    call printf
                
    
        
        mov rdi, asm_ret_msg
        xor rax, rax
        call printf
        pop rbp
        ret
        