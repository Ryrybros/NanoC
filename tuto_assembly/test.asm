extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a : dq 0
   global main
    section .text
            ;This is a function
            m:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 48
                mov qword [rbp - 8],0
mov qword [rbp - 16],0
mov qword [rbp - 24],0
mov qword [rbp - 32],0

            
            mov rax, 4
            mov [rbp - 8] , rax
            
            mov rax, 6
            mov [rbp - 16] , rax
            
            lea rax, [rbp - 8]
            mov [rbp - 24] , rax
            
            lea rax, [rbp - 24]
            mov [rbp - 32] , rax
            
                   
     
            mov rax, 3
            push rax
             
            mov rax, 3
            push rax
             
            mov rax, 2
            push rax
             
            mov rax, 2
            push rax
            mov rax, [rbp - 32]
            pop rbx
            add rax, rbx
            
        
            pop rbx
            sub rax, rbx
            
        
            pop rbx
            add rax, rbx
            
        
            pop rbx
            sub rax, rbx
            
             

            push rax
            lea rax, [rbp - 16]
            pop rbx
            mov [rbx] , rax
                    
    mov rax, [rbp - 32]     
    mov rax, [rax]
      
    mov rax, [rax]
                    push rdi
                    push rsi
                    push rax
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                    pop rax
                    pop rsi
                    pop rdi
                
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
            ;This is a function call


call m;end_func_call

            mov [a] , rax
            
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            