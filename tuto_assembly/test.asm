extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    n : dq 0
T1 : dq 0
T2 : dq 0
T3 : dq 0
   global main
    section .text
            ;This is a function
            print_tab:                    ;Name of func

            push rbp
            mov rbp, rsp
            mov qword [rbp - 24],0

            mov rax, 0
        mov r11, rax
        for_0:
        mov rax, rsi
        push rax
        mov rax, r11
        pop rbx
        cmp rax, rbx
        jge end_for_0

                
     
             
            mov rax, r11
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
                    push r11
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
            pop r11

                
                    
                    

                    mov rax, 0x00
                    push rax


                    

                        mov rax, 0x0000000000202C20
                        push rax 

                        
                    mov rax, rsp
                    push r11
            push rdi ; saving rdi
            
            push rsi ; saving rsi
            
            push rdx ; saving rdx
            
            push rcx ; saving rcx
            
            push r8 ; saving r8
            
            push r9 ; saving r9
            

                    push rax
                    mov rdi, rax
                    xor rax, rax
                    call printf
                    pop rax
                    
            pop r9
            
            pop r8
            
            pop rcx
            
            pop rdx
            
            pop rsi
            
            pop rdi
            pop r11
                    
                    add rsp, 16
                

        mov rax, 1
        push rax
        mov rax, r11
        pop rbx
        add rax, rbx
        mov r11, rax
        
        jmp for_0
        end_for_0:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            ;This is a function
            standard:                    ;Name of func

            push rbp
            mov rbp, rsp
            mov qword [rbp - 32],0

            mov rax, 0
        mov r11, rax
        for_1:
        mov rax, rsi
        push rax
        mov rax, r11
        pop rbx
        cmp rax, rbx
        jge end_for_1

        
                   
     
             
            mov rax, r11
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
             
            mov rax, rdx
            push rax
            mov rax, r11
            pop rbx
            add rax, rbx
            
        
            pop rbx
            mov [rbx] , rax
            

        mov rax, 1
        push rax
        mov rax, r11
        pop rbx
        add rax, rbx
        mov r11, rax
        
        jmp for_1
        end_for_1:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            ;This is a function
            shuffled:                    ;Name of func

            push rbp
            mov rbp, rsp
            mov qword [rbp - 32],0

            mov rax, 0
        mov r11, rax
        for_2:
        mov rax, rsi
        push rax
        mov rax, r11
        pop rbx
        cmp rax, rbx
        jge end_for_2

        
                   
     
             
            mov rax, r11
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
             
            
         
            
         
            mov rax, rdx
            push rax
            mov rax, r11
            pop rbx
            add rax, rbx
            
        
        
            push rax
            mov rax, 10
            pop rbx
            sub rax, rbx
            
        
        
            push rax
             
            
         
            mov rax, rdx
            push rax
            mov rax, r11
            pop rbx
            add rax, rbx
            
        
        
            push rax
            
         
            
         
            mov rax, rdx
            push rax
            mov rax, r11
            pop rbx
            add rax, rbx
            
        
        
            push rax
            mov rax, 5
            pop rbx
            sub rax, rbx
            
        
        
            pop rbx
            imul  rax, rbx
            
        
            pop rbx
            imul  rax, rbx
            
        
            pop rbx
            mov [rbx] , rax
            

        mov rax, 1
        push rax
        mov rax, r11
        pop rbx
        add rax, rbx
        mov r11, rax
        
        jmp for_2
        end_for_2:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi

            

            
            
            mov rax, 3
            mov [n] , rax
            
            
     
            mov rax, 8
            push rax
            mov rax, [n]
            pop rbx
            imul  rax, rbx
            
        
    push r11
            push rdi ; saving rdi
            
            push rsi ; saving rsi
            
            push rdx ; saving rdx
            
            push rcx ; saving rcx
            
            push r8 ; saving r8
            
            push r9 ; saving r9
            
    mov rdi, rax
    call malloc
    
            pop r9
            
            pop r8
            
            pop rcx
            
            pop rdx
            
            pop rsi
            
            pop rdi
            pop r11
    
            mov [T1] , rax
            
            ;This is a function call

                push rdi
                
                
                push rsi
                
                
                push rdx
                
                
;start arg scipt 
        mov rax, [T1]
                push rax

                mov rax, [n]
                push rax

                mov rax, 0
                push rax

                ; here for arg


                pop rdx
                
                pop rsi
                
                pop rdi
                
call shuffled;end_func_call

                pop rdx
                
                pop rsi
                
                pop rdi
                
        
            ;This is a function call

                push rdi
                
                
                push rsi
                
                
;start arg scipt 
        mov rax, [T1]
                push rax

                mov rax, [n]
                push rax

                ; here for arg


                pop rsi
                
                pop rdi
                
call print_tab;end_func_call

                pop rsi
                
                pop rdi
                
        
            
            mov rdi, asm_ret_msg
            xor rax, rax
            call printf
            pop rbp
            ret
            