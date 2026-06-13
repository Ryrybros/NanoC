extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    asm_static_tab_T times 3 dq 0
            T : dq 0
   global main
    section .text
            ;This is a function
            fill:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 32
                mov qword [rbp - 16],0
mov qword [rbp - 24],0

            
            mov rax, 3
            mov [rbp - 16] , rax
            
        while_0:
             
            mov rax, [rbp - 16]
            push rax
            mov rax, [rbp - 24]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_0
            
                   
     
             
            mov rax, [rbp - 24]
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
             
            mov rax, 10
            push rax
             
            mov rax, [rbp - 24]
            push rax
            mov rax, [rbp - 24]
            pop rbx
            imul  rax, rbx
            
        
            pop rbx
            add rax, rbx
            
        
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 24]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 24] , rax
            
            jmp while_0
        end_while_0:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            ;This is a function
            print_tab:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 32
                mov qword [rbp - 16],0
mov qword [rbp - 24],0

            
            mov rax, 3
            mov [rbp - 24] , rax
            
            mov rax, 0
            mov [rbp - 16] , rax
            
        while_1:
             
            mov rax, [rbp - 24]
            push rax
            mov rax, [rbp - 16]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_1
                    
     
             
            mov rax, [rbp - 16]
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
                    
            push rdi ; saving rdi
            
            push rsi ; saving rsi
            
            push rdx ; saving rdx
            
            push rcx ; saving rcx
            
            push r8 ; saving r8
            
            push r9 ; saving r9
            
                    push rax
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                    pop rax
                    
            pop r9
            
            pop r8
            
            pop rcx
            
            pop rdx
            
            pop rsi
            
            pop rdi
            

                
                    
                    

                    mov rax, 0x00
                    push rax


                    

                    mov rax, 0x0000000000202C20
                    push rax 

                    

                    
            push rdi ; saving rdi
            
            push rsi ; saving rsi
            
            push rdx ; saving rdx
            
            push rcx ; saving rcx
            
            push r8 ; saving r8
            
            push r9 ; saving r9
            

                    push rax
                    mov rdi, rsp
                    xor rax, rax
                    call printf
                    pop rax
                    
            pop r9
            
            pop r8
            
            pop rcx
            
            pop rdx
            
            pop rsi
            
            pop rdi
            
                    
                    add rsp, 16
                
             
            mov rax, 1
            push rax
            mov rax, [rbp - 16]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 16] , rax
            
            jmp while_1
        end_while_1:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi

            mov rax, asm_static_tab_T
            mov [T], rax


            
            
            ;This is a function call

                push rdi
                
                
mov rax, [T]
                push rax
                


                pop rdi
                
call fill;end_func_call

                pop rdi
                
        
            ;This is a function call

                push rdi
                
                
mov rax, [T]
                push rax
                


                pop rdi
                
call print_tab;end_func_call

                pop rdi
                
        
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            