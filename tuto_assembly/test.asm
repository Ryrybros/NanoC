extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a : dq 8
endl : db " ",10," ", 0
e: dq 0 
x : dq 10
s : db "HEllo world ",10," ", 0
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
        jz end_2
        
        mov rax, 1
        mov rsp, rbp           
        pop rbp     
        ret
        
        jmp end_else_2
        end_2:
        
         
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
        
        end_else_2:
            
            
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
                    xor rax, rax
                    call printf
                
                    mov rdi, asm_int_prtr
                    mov rsi, [a]
                    xor rax, rax
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
                    xor rax, rax
                    call printf
                
                    mov rdi, endl
                    xor rax, rax
                    call printf
                
                    mov rdi, s
                    xor rax, rax
                    call printf
                
        while_0:
             
        mov rax, 0
        push rax
        mov rax, [x]
        pop rbx
        cmp rax, rbx
        setg al
        movzx rax, al
    
            cmp rax, 0
            jz end_while_0
            
                    mov rdi, asm_int_prtr
                    mov rsi, [x]
                    xor rax, rax
                    call printf
                
                    mov rdi, endl
                    xor rax, rax
                    call printf
                
                     
        mov rax, 1
        push rax
        mov rax, [x]
        pop rbx
        sub rax, rbx
        
    
                    mov qword [x] , rax
            
            jmp while_0
        end_while_0:
        
        mov rax, [x]
        cmp rax, 0
        jz end_1
         
        mov rax, 100
        push rax
        mov rax, [x]
        pop rbx
        add rax, rbx
        
    
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                
        jmp end_else_1
        end_1:
         
        mov rax, 200
        push rax
        mov rax, [x]
        pop rbx
        add rax, rbx
        
    
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                
        end_else_1:
        
                    mov rdi, endl
                    xor rax, rax
                    call printf
                
        
        mov rdi, asm_ret_msg
        xor rax, rax
        call printf
        pop rbp
        ret
        