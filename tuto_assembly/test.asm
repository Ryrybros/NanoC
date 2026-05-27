extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    c : dq 10
endl : db " ",10," ", 0
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
        jz end_0
        
        mov rax, rdi
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
        
        end_else_0:
            
            
            ;This is a function
            hallo:                    ;Name of func

            push rbp
            mov rbp, rsp
            
            
         
        mov rax, rdi
        push rax
        mov rax, rdi
        pop rbx
        imul  rax, rbx
        
    
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
            ;This is a function call
mov rax, [c]
            push rdi
            mov rdi , rax
            

call fib;end_func_call

            pop rdi
            
            mov qword [c] , rax
            
                    mov rdi, endl
                    xor rax, rax
                    call printf
                
                    mov rdi, asm_int_prtr
                    mov rsi, [c]
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
            