extern printf; e.g stdio.h
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    x : dq 10
s : db "HEllo world ",10," ", 0
endl : db " ",10," ", 0
   global main
    section .text
            ;This is a function
            hello:                    ;Name of func
            
                    push rbp
                    mov rbp, rsp
                    sub rsp, 16
                mov qword [rbp - 8],2

            
                     
        mov rax, 10
        push rax
        mov rax, [rbp - 8]
        pop rbx
        add rax, rbx
        
    
                    mov [rbp - 8] , rax
            
                    mov rdi, asm_int_prtr
                    mov rsi, [rbp - 8]
                    xor rax, rax
                    call printf
                
            mov rax, [rbp - 8]
            mov rsp, rbp              
            pop rbp     
            ret
            
        main:
        push rbp            
        mov rbp, rsp
        
            call hello
        
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
        
    
                    mov [x] , rax
            
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
        
        
        mov rdi, asm_ret_msg
        xor rax, rax
        call printf
        pop rbp
        ret
        