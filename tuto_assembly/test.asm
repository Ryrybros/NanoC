extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a : dq 0
b : dq 0
c : dq 0
e : dq 0
   global main
    section .text
            ;This is a function
            g:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    
                    sub rsp, 32
                mov qword [rbp - 8],0
mov qword [rbp - 16],0

            
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            ;This is a function
            f:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    
                    sub rsp, 32
                mov qword [rbp - 8],0
mov qword [rbp - 16],0

            
                     
            mov rax, rsi
            push rax
             
            ;This is a function call
mov rax, rdi
            push rdi
            mov rdi , rax
            mov rax, [rbp - 8]
            push rsi
            mov rsi , rax
            

call g;end_func_call

            pop rdi
            
            pop rsi
            
            push rax
            mov rax, rsi
            pop rbx
            imul  rax, rbx
            
        
            pop rbx
            add rax, rbx
            
        
                    mov qword [rbp - 8] , rax
                
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

                    ;This is a function call
mov rax, [e]
            push rdi
            mov rdi , rax
            mov rax, 0
            push rsi
            mov rsi , rax
            

call f;end_func_call

            pop rdi
            
            pop rsi
            
                    mov qword [a] , rax
                
                    mov rdi, asm_int_prtr
                    mov rsi, [a]
                    xor rax, rax
                    call printf
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            