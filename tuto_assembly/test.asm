extern printf; e.g stdio.h
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    a : dq 5
endl : db " ",10," ", 0
   global main
    section .text
            ;This is a function
            fact:                    ;Name of func

            push rbp
            mov rbp, rsp
            
            
         
        mov rax, 1
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
            

call fact;end_func_call

            pop rdi
            
        push rax
        mov rax, rdi
        pop rbx
        imul  rax, rbx
        
    
        mov rsp, rbp           
        pop rbp     
        ret
        
        end_else:
            
            
        main:
        push rbp            
        mov rbp, rsp
        
            ;This is a function call
mov rax, [a]
            push rdi
            mov rdi , rax
            

call fact;end_func_call

            pop rdi
            
            mov qword [a] , rax
            
                    mov rdi, endl
                    call printf
                
                    mov rdi, asm_int_prtr
                    mov rsi, [a] 
                    call printf
                
    
        
    mov rdi, asm_ret_msg
    call printf
    pop rbp
    ret
    