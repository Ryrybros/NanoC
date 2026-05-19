import os
import lark

path = "cours_script"
grammar_path = "cours_grammar"
with open(path) as f:
    script = f.read()
with open(grammar_path) as f:
    grammar = f.read()

gram = f''' {grammar} '''

l = lark.Lark(gram,start="main")
# tree = l.parse(script)
# print( tree.pretty() )

#The code is parsed

cpt_if_while = [-1]

def pp_expression(ast):
    
    if ast.data in  ( "variable" , "int"  ):
        return ast.children[0].value
    lo = f"{pp_expression(ast.children[0])}"
    op = f"{ast.children[1].value}"
    ro = f"{pp_expression(ast.children[2])}"
    return lo + " " + op + " " + ro


def asm_expression(ast):
    if ast.data in  ( "variable" , "int" ):
        if ast.data == "variable":
            return f"mov rax, [{ast.children[0].value}]"
        else: return f"mov rax, {ast.children[0].value}"
    
    op = f"{ast.children[1].value}"
    command = "no command"
    if op == "+" : command = "add"
    if op == "-" : command = "sub"
    if op == "*" : command = "imul "
    if op == "/" : command = "div"#"div " + lo + " , " + ro
    boolean = ""
    if op == "<" : 
        command = "cmp"
        boolean = f"""setl al
        movzx rax, al"""
    
    if op == "<=" : 
        command = "cmp"
        boolean = f"""setle al
        movzx rax, al"""
    

    if op == ">" : 
        command = "cmp"
        boolean = f"""setg al
        movzx rax, al"""
    

    if op == ">=" : 
        command = "cmp"
        boolean = f"""setge al
        movzx rax, al"""

    
    if op == "==" : 
        command = "cmp"
        boolean = f"""sete al
        movzx rax, al"""

    

    return f""" 
        {asm_expression(ast.children[2])}
        push rax
        {asm_expression(ast.children[0])}
        pop rbx
        {command} rax, rbx
        {boolean}
    """

    






def pp_args(ast):
    if ast.data == "var":
        variable = ast.children[0].value 
        return variable
    if ast.data == "arglist":
        arglist = ast.children
        res =  f"{arglist[0].children[0].value}"
        if len(ast.children) > 1 :
            for i in range(1 ,len(ast.children)):
                res += f" , {ast.children[i].children[0].value}"
        return res
    
def pp_command(ast):
    
    if ast.data == "assignment":
        lvalue = ast.children[0].value
        rvalue = pp_expression(ast.children[1])
        return f"{lvalue}  =  {rvalue}"
    if ast.data == "sequence":
        command = pp_command(ast.children[0])
        following = pp_command(ast.children[1])
        return f"{command}\n{following}"

    if ast.data == "if_else":
        test = pp_expression(ast.children[0].children[0])
        script = pp_command(ast.children[0].children[1])
        res =  f"if ( {test} ) \n  {script} "
        if len(ast.children) > 1:
            escript = pp_command(ast.children[1].children[0])
            res += f"\nelse\n  {escript} "
        return res
    
    if ast.data == "while":
        test = pp_expression(ast.children[0])
        script = pp_command(ast.children[1])
        return  f"while ( {test} ) \n  xor al , al {script} "
        

    if ast.data == "main":
        args = pp_args(ast.children[0])
        script = pp_command(ast.children[1])
        returned = pp_expression(ast.children[2].children[0])
        return f"main ( {args} )\n {script} \n return {returned}  "


    return "Wrong or not implemented"

def asm_declare_vars_list(ast, vars):
    # Cette fonction dans certains cas renvoie une string, d'autre fois modif par effet de bord une liste
    if ast.data in ( 'variable' , 'int', "bin", 'assignment', 'format_str', 'format_int','function','function_call') : return 
    if ast.data == 'declaration' :
        # print(ast)
        if len(ast.children) == 1:
            return ast.children[0].children[0] + ": dq 0 " 
        elif len(ast.children) == 2:
            alloc_command = "dq"
            printed_string = ast.children[1].value
            if ast.children[1].type == "STRING": 
                alloc_command = "db" 
                printed_string = str(ast.children[1])
                printed_string = printed_string.replace(r"\n",  ' ",10," ' )
                return ast.children[0].children[0] + f" : {alloc_command} " + printed_string + ", 0"
            return ast.children[0].children[0] + f" : {alloc_command} " + printed_string  
            
    else:
        for i in range(len(ast.children)):
            val = asm_declare_vars_list( ast.children[i] , vars )
            if val != None: vars.append(val)

def asm_init_vars_main(ast):
    if len(ast.children) > 0:
        assert(ast.data == "arglist")
        decl_var = ""
        init_var = ""
        for i in range(len(ast.children)):
            v = ast.children[i].children[0]
            decl_var += f"{v} : dq 0\n"
            init_var += f"""mov rbx, [argv]
mov rdi, [rbx+{(i+1)*8}]
call atoi
mov [{v}], rax
"""
        return decl_var, init_var
    
    assert(ast.data == "no_var")
    return "", ""


def asm_infunc_declare_vars_list(ast, vars):
    if ast.data in ( 'variable' , 'int', "bin", 'assignment', 'format_str', 'format_int','function','function_call') : return 
    if ast.data == 'declaration' :
        # print(ast)
        if len(ast.children) == 1:
            return (ast.children[0].children[0].value, "0") 
        elif len(ast.children) == 2:
            alloc_command = "dq"
            printed_string = ast.children[1].value
            if ast.children[1].type == "STRING": 
                alloc_command = "db" 
                printed_string = str(ast.children[1])
                printed_string = printed_string.replace(r"\n",  ' ",10," ' )
                return ast.children[0].children[0] + f" : {alloc_command} " + printed_string + ", 0"
            return (ast.children[0].children[0].value, printed_string)
            
    else:
        for i in range(len(ast.children)):
            
            val = asm_infunc_declare_vars_list( ast.children[i] , vars )
            if val != None: vars.append(val)


def asm_declare_vars(vars : list):
    ret = ""
    for var in vars: ret += f"{var}\n"
    return ret




def asm_command(ast):
    
    if ast.data == "assignment":
        if ast.children[1].data == 'int':
            return "mov qword [" + ast.children[0] + "] , " + ast.children[1].children[0].value

        if ast.children[1].data == 'bin':
            
            return f"""
                    {asm_expression(ast.children[1])}
                    mov [{ast.children[0].value}] , rax
            """

    if ast.data == "declaration":
        return ""
         

    if ast.data == "sequence":
        
        command = asm_command(ast.children[0])
        following = asm_command(ast.children[1])

        return f"{command}{following}"

    if ast.data == "if_else":
        test = asm_expression(ast.children[0].children[0])
        script = asm_command(ast.children[0].children[1])
        script_else = asm_command(ast.children[1].children[0])

        cpt_if_while[0] += 1

        return f"""
        {test}
        cmp rax, 0
        jz end_{cpt_if_while[0]}
        {script}
        jmp end_else_{cpt_if_while[0]}
        end_{cpt_if_while[0]}:
        {script_else}
        end_else_{cpt_if_while[0]}:
        """

    if ast.data == "pass":
        return """nop
        """
        
    if ast.data == "while":        
        test = asm_expression(ast.children[0])
        script = asm_command(ast.children[1])
        cpt_if_while[0] += 1

        return  f"""
        while_{cpt_if_while[0]}:
            {test}
            cmp rax, 0
            jz end_while_{cpt_if_while[0]}
            {script}
            jmp while_{cpt_if_while[0]}
        end_while_{cpt_if_while[0]}:
        """

    if ast.data == "print":
        if ast.children[1].data == "variable":
            if ast.children[0].children[0] == "str":
                return f"""
                    mov rdi, {ast.children[1].children[0]}
                    xor rax, rax
                    call printf
                """
            elif ast.children[0].children[0] == "int" :
                return f"""
                    mov rdi, asm_int_prtr
                    mov rsi, [{ast.children[1].children[0]}]
                    xor rax, rax
                    call printf
                """
        else : 
            
            stret = asm_expression(ast.children[1])
            
            if ast.children[0].children[0] == "int" :
                return stret + f"""
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                """
    
    if ast.data == "function_call":
        # print(ast)
        return f"""
            call {ast.children[0].children[0]}
        """

    return "Wrong or not implemented"


    
def asm_func(ast):
    
    for child in ast.children:
        if child.data == "function":
            vars = []
            asm_infunc_declare_vars_list(child.children[2], vars)
            
            if len(vars) != 0:
                var_dec = f"""
                    push rbp
                    mov rbp, rsp
                    sub rsp, {int(8*len(vars) / 16) + 16}
                """
            else: var_dec = ""
            script = asm_command(child.children[2])
            returned = asm_expression(child.children[3].children[0])
            for  i in range(len(vars)):
                var_dec += f"mov qword [rbp - {8*(i+1)}],{vars[i][1]}\n" 
                script = script.replace(vars[i][0], f"rbp - {(i+1)*8}" )
                returned = returned.replace(vars[i][0], f"rbp - {(i+1)*8}" )

            return f"""
            ;This is a function
            {child.children[0]}:                    ;Name of func
            {var_dec}
            {script}
            {returned}
            mov rsp, rbp              
            pop rbp     
            ret
            """

def asm_main(ast):

    if ast.data == "main":
        decl_vars_main, init_vars_main = asm_init_vars_main(ast.children[0])
        print(decl_vars_main, init_vars_main)
        script = asm_command(ast.children[1])
        returned = asm_expression(ast.children[2].children[0])
        # Ignore completement le returned
        return f"""
        main:
        push rbp            
        mov rbp, rsp
        mov [argv], rsi
        {init_vars_main}
        {script}
        
        mov rdi, asm_ret_msg
        xor rax, rax
        call printf
        pop rbp
        ret
        """, decl_vars_main
    
    
    return "Wrong or not implemented", "Wrong or not implemented"
    
def assembly(script):
    vars = []
    l = lark.Lark(gram, start= "main")
    t = l.parse(script)

    asm_script = """extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    """

    main_prog, init_vars_main = asm_main(t)

    asm_script += init_vars_main

    asm_declare_vars_list(t, vars)
    asm_script +=  asm_declare_vars(vars)

    asm_script += """   global main
    section .text"""
    if asm_func(t) != None:    
        asm_script += asm_func(t)


    asm_script += main_prog
    

    # print(asm_command(t))
    print(asm_script)
    with open("tuto_assembly/test.asm", "w") as f:
        f.write(asm_script)
    os.system("./tuto_assembly/build.sh tuto_assembly/test.asm")



if __name__ == '__main__':
    # l2 = lark.Lark(string,start="main")
    # tasm = l2.parse("main(x){int x ; while(x < 10 ) {x = x +1; int z = 0; }return 0 ;}")
    # # print(asm_command(tasm))
    # vars = []
    # asm_declare_vars(tasm, vars)
    # print(vars)
    assembly(script)