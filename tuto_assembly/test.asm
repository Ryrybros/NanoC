extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    T : dq 0
T2 : dq 0
R : dq 0
s : dq 0
s2 : dq 0
   global main
    section .text
            ;This is a function
            print_tab:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 48
                mov qword [rbp - 24],0

            
            mov rax, 0
            mov [rbp - 24] , rax
            
        while_0:
             
            mov rax, rsi
            push rax
            mov rax, [rbp - 24]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_0
                    
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 24]
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
            standard:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 32
                mov qword [rbp - 32],0

            
            mov rax, 0
            mov [rbp - 32] , rax
            
        while_1:
             
            mov rax, rsi
            push rax
            mov rax, [rbp - 32]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_1
            
                   
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 32]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
             
            mov rax, rdx
            push rax
            mov rax, [rbp - 32]
            pop rbx
            add rax, rbx
            
        
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 32]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 32] , rax
            
            jmp while_1
        end_while_1:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            ;This is a function
            shuffled:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 48
                mov qword [rbp - 32],0

            
            mov rax, 0
            mov [rbp - 32] , rax
            
        while_2:
             
            mov rax, rsi
            push rax
            mov rax, [rbp - 32]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_2
            
                   
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 32]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
             
            
         
            
         
            mov rax, rdx
            push rax
            mov rax, [rbp - 32]
            pop rbx
            add rax, rbx
            
        
        
            push rax
            mov rax, 10
            pop rbx
            sub rax, rbx
            
        
        
            push rax
             
            
         
            mov rax, rdx
            push rax
            mov rax, [rbp - 32]
            pop rbx
            add rax, rbx
            
        
        
            push rax
            
         
            
         
            mov rax, rdx
            push rax
            mov rax, [rbp - 32]
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
            mov rax, [rbp - 32]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 32] , rax
            
            jmp while_2
        end_while_2:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            ;This is a function
            concat:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 48
                mov qword [rbp - 48],0

            
            mov rax, 0
            mov [rbp - 48] , rax
            
        while_3:
             
            mov rax, rsi
            push rax
            mov rax, [rbp - 48]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_3
            
                   
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 48]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, r8
            pop rbx
            add rax, rbx
            
             

            push rax
                    
     
            
         
            mov rax, [rbp - 48]
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 48]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 48] , rax
            
            jmp while_3
        end_while_3:
        
        while_4:
             
            
         
            mov rax, rcx
            push rax
            mov rax, rsi
            pop rbx
            add rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 48]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_4
            
                   
     
            
         
            mov rax, [rbp - 48]
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, r8
            pop rbx
            add rax, rbx
            
             

            push rax
                    
     
            
         
            
         
            mov rax, rsi
            push rax
            mov rax, [rbp - 48]
            pop rbx
            sub rax, rbx
            
        
        
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdx
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 48]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 48] , rax
            
            jmp while_4
        end_while_4:
        
        mov rax, r8
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            ;This is a function
            merge:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 112
                mov qword [rbp - 40],0
mov qword [rbp - 48],0
mov qword [rbp - 56],0
mov qword [rbp - 64],0
mov qword [rbp - 72],0
mov qword [rbp - 80],0
mov qword [rbp - 88],0

            
             
            mov rax, 1
            push rax
             
            mov rax, rsi
            push rax
            mov rax, rdx
            pop rbx
            sub rax, rbx
            
        
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 64] , rax
            
             
            mov rax, rdx
            push rax
            mov rax, rcx
            pop rbx
            sub rax, rbx
            
        
            mov [rbp - 72] , rax
            
            
     
            mov rax, 8
            push rax
            mov rax, [rbp - 64]
            pop rbx
            imul  rax, rbx
            
        
    
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
            
    
            mov [rbp - 80] , rax
            
            
     
            mov rax, 8
            push rax
            mov rax, [rbp - 72]
            pop rbx
            imul  rax, rbx
            
        
    
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
            
    
            mov [rbp - 88] , rax
            
            mov rax, 0
            mov [rbp - 40] , rax
            
            mov rax, 0
            mov [rbp - 48] , rax
            
        while_5:
             
            mov rax, [rbp - 64]
            push rax
            mov rax, [rbp - 40]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_5
            
                   
     
            
         
            mov rax, [rbp - 40]
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 80]
            pop rbx
            add rax, rbx
            
             

            push rax
                    
     
            
         
            mov rax, 8
            push rax
            
         
            
        mov rax, [rbp - 40]
        
            push rax
            mov rax, rsi
            pop rbx
            add rax, rbx
            
        
        
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 40]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 40] , rax
            
            jmp while_5
        end_while_5:
        
        while_6:
             
            mov rax, [rbp - 72]
            push rax
            mov rax, [rbp - 48]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_6
            
                   
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 48]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 88]
            pop rbx
            add rax, rbx
            
             

            push rax
                    
     
            
         
            
         
            mov rax, [rbp - 48]
            push rax
             
            mov rax, 1
            push rax
            mov rax, rdx
            pop rbx
            add rax, rbx
            
        
            pop rbx
            add rax, rbx
            
        
        
            push rax
            mov rax, 8
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 48]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 48] , rax
            
            jmp while_6
        end_while_6:
        
            mov rax, 0
            mov [rbp - 40] , rax
            
            mov rax, 0
            mov [rbp - 48] , rax
            
            mov rax, rsi
            mov [rbp - 56] , rax
            
        while_8:
             
            
         
            mov rax, [rbp - 72]
            push rax
            mov rax, [rbp - 48]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
        
            push rax
            
         
            mov rax, [rbp - 64]
            push rax
            mov rax, [rbp - 40]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
        
            pop rbx
            and rax, rbx
            
        
            cmp rax, 0
            jz end_while_8
            
         
                    
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 48]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 88]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            push rax
                    
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 40]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 80]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            cmp rax, rbx
            setle al
            movzx rax, al
        
        cmp rax, 0
        jz end_7
        
                   
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 56]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
                    
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 40]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 80]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 40]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 40] , rax
            
        jmp end_else_7
        end_7:
        
                   
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 56]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
                    
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 48]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 88]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 48]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 48] , rax
            
        end_else_7:
        
             
            mov rax, 1
            push rax
            mov rax, [rbp - 56]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 56] , rax
            
            jmp while_8
        end_while_8:
        
        while_9:
             
            mov rax, [rbp - 64]
            push rax
            mov rax, [rbp - 40]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_9
            
                   
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 56]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
                    
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 40]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 80]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 40]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 40] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 56]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 56] , rax
            
            jmp while_9
        end_while_9:
        
        while_10:
             
            mov rax, [rbp - 72]
            push rax
            mov rax, [rbp - 48]
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
            cmp rax, 0
            jz end_while_10
            
                   
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 56]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, rdi
            pop rbx
            add rax, rbx
            
             

            push rax
                    
     
            
         
            mov rax, 8
            push rax
            mov rax, [rbp - 48]
            pop rbx
            imul  rax, rbx
            
        
        
            push rax
            mov rax, [rbp - 88]
            pop rbx
            add rax, rbx
            
             
      
    mov rax, [rax]
            pop rbx
            mov [rbx] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 48]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 48] , rax
            
             
            mov rax, 1
            push rax
            mov rax, [rbp - 56]
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 56] , rax
            
            jmp while_10
        end_while_10:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            ;This is a function
            mergeSort:                    ;Name of func

            push rbp
            mov rbp, rsp
            
                    ; function args > nb_registers = 0
                    sub rsp, 48
                mov qword [rbp - 32],0

            
         
            mov rax, rdx
            push rax
            mov rax, rsi
            pop rbx
            cmp rax, rbx
            setl al
            movzx rax, al
        
        cmp rax, 0
        jz end_11
        
             
            
        
            mov rax, 2
            push rax
            
         
            mov rax, rsi
            push rax
            mov rax, rdx
            pop rbx
            sub rax, rbx
            
        
        
            pop rbx
            push rdx
            xor rdx, rdx
            div rbx
            pop rdx
            
        
            push rax
            mov rax, rsi
            pop rbx
            add rax, rbx
            
        
            mov [rbp - 32] , rax
            
            ;This is a function call

                push rdi
                
                
                push rsi
                
                
                push rdx
                
                
mov rax, rdi
                push rax
                mov rax, rsi
                push rax
                mov rax, [rbp - 32]
                push rax
                


                pop rdx
                
                pop rsi
                
                pop rdi
                
call mergeSort;end_func_call

                pop rdx
                
                pop rsi
                
                pop rdi
                
        
            ;This is a function call

                push rdi
                
                
                push rsi
                
                
                push rdx
                
                
mov rax, rdi
                push rax
                 
            mov rax, 1
            push rax
            mov rax, [rbp - 32]
            pop rbx
            add rax, rbx
            
        
                push rax
                mov rax, rdx
                push rax
                


                pop rdx
                
                pop rsi
                
                pop rdi
                
call mergeSort;end_func_call

                pop rdx
                
                pop rsi
                
                pop rdi
                
        
            ;This is a function call

                push rdi
                
                
                push rsi
                
                
                push rdx
                
                
                push rcx
                
                
mov rax, rdi
                push rax
                mov rax, rsi
                push rax
                mov rax, [rbp - 32]
                push rax
                mov rax, rdx
                push rax
                


                pop rcx
                
                pop rdx
                
                pop rsi
                
                pop rdi
                
call merge;end_func_call

                pop rcx
                
                pop rdx
                
                pop rsi
                
                pop rdi
                
        
        jmp end_else_11
        end_11:
        nop
        
        end_else_11:
        
        mov rax, 0
        mov rsp, rbp           
        pop rbp     
        ret
            
            
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi
            
            
            mov rax, 10
            mov [s] , rax
            
            
     
            mov rax, 8
            push rax
            mov rax, [s]
            pop rbx
            imul  rax, rbx
            
        
    
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
            
    
            mov [T] , rax
            
            
     
            mov rax, 8
            push rax
            mov rax, [s]
            pop rbx
            imul  rax, rbx
            
        
    
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
            
    
            mov [T2] , rax
            
             
            mov rax, 8
            push rax
             
            mov rax, [s]
            push rax
            mov rax, 2
            pop rbx
            imul  rax, rbx
            
        
            pop rbx
            imul  rax, rbx
            
        
            mov [s2] , rax
            
            ;This is a function call

                push rdi
                
                
                push rsi
                
                
                push rdx
                
                
mov rax, [T]
                push rax
                mov rax, [s]
                push rax
                mov rax, 0
                push rax
                


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
                
                
mov rax, [T]
                push rax
                mov rax, [s]
                push rax
                


                pop rsi
                
                pop rdi
                
call print_tab;end_func_call

                pop rsi
                
                pop rdi
                
        
            ;This is a function call

                push rdi
                
                
                push rsi
                
                
                push rdx
                
                
mov rax, [T]
                push rax
                mov rax, 0
                push rax
                 
            mov rax, 1
            push rax
            mov rax, [s]
            pop rbx
            sub rax, rbx
            
        
                push rax
                


                pop rdx
                
                pop rsi
                
                pop rdi
                
call mergeSort;end_func_call

                pop rdx
                
                pop rsi
                
                pop rdi
                
        
             
            mov rax, [s]
            push rax
            mov rax, 2
            pop rbx
            imul  rax, rbx
            
        
            mov [s2] , rax
            
                    
                    

                    mov rax, 0x00
                    push rax


                    

                    mov rax, 0x0000000000000000
                    push rax 

                    

                    mov rax, 0x0020206C616E6946
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
            
                    
                    add rsp, 24
                
            ;This is a function call

                push rdi
                
                
                push rsi
                
                
mov rax, [T]
                push rax
                mov rax, [s]
                push rax
                


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
            