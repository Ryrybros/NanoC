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
                    call printf
                
        while:
             
        mov rax, 0
        push rax
        mov rax, [x]
        pop rbx
        cmp rax, rbx
        setg al
        movzx rax, al
    
            cmp rax, 0
            jz end_while
            
                    mov rdi, asm_int_prtr
                    mov rsi, [x]
                    call printf
                
                    mov rdi, endl
                    call printf
                
                     
        mov rax, 1
        push rax
        mov rax, [x]
        pop rbx
        sub rax, rbx
        
    
                    mov [x] , rax
            
            jmp while
        end_while:
        
    
        
    mov rdi, asm_ret_msg
    call printf
    pop rbp
    ret
    