extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    a : dq 0
b : dq 0
c : dq 0
d : dq 0
e : dq 0
t : dq 0
x : dq 0
   global main
    section .text
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
                    mov rax, 4
                    mov qword [a] , rax
                       
    mov rax, QWORD a
    mov [d], rax
       
    mov rax, QWORD d
    mov [c], rax
       
    mov rax, QWORD c
    mov [b], rax
       
    mov rax, QWORD b
    mov [e], rax
       
    mov rax, QWORD b
    mov [t], rax

                            
     
            
         
            mov rax, [a]
            push rax
            mov rax, 9
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
             
            
         
            mov rax, [a]
            push rax
            mov rax, 9
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
                    
     
            mov rax, 8
            push rax
             
            
         
            mov rax, [a]
            push rax
            mov rax, 2
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
             
            mov rax, 8
            push rax
             
            
         
            mov rax, 2
            push rax
            mov rax, [a]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [e]
            pop rbx
            add rax, rbx
            
        
            pop rbx
            add rax, rbx
            
        
            pop rbx
            sub rax, rbx
            
        
            pop rbx
            sub rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            add rax, rbx
            
        
            pop rbx
            sub rax, rbx
            
             
    mov rax, [rax]
    mov rax, [rax]
      
    mov rax, [rax]
                    mov qword [x] , rax
                
                    mov rdi, asm_int_prtr
                    mov rsi, [x]
                    xor rax, rax
                    call printf
                    add rsp, 16
                
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            