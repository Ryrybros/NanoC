extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a : dq 0
zaza : dq 0
b : dq 0
c : dq 0
   global main
    section .text
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
            mov rax, 4
            mov [a] , rax
            
            mov rax, 6
            mov [zaza] , rax
            
            mov rax, QWORD a
            mov [b] , rax
            
            mov rax, QWORD b
            mov [c] , rax
            
                   
     
            mov rax, 3
            push rax
             
            mov rax, 3
            push rax
             
            mov rax, 2
            push rax
             
            mov rax, 2
            push rax
            mov rax, [c]
            pop rbx
            add rax, rbx
            
        
            pop rbx
            sub rax, rbx
            
        
            pop rbx
            add rax, rbx
            
        
            pop rbx
            sub rax, rbx
            
             

            push rax
            mov rax, QWORD zaza
            pop rbx
            mov [rbx] , rax
                    
    mov rax, [c]     
    mov rax, [rax]
      
    mov rax, [rax]
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            