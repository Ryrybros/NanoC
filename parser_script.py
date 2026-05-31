import os
import lark
# from pretty_printer_script import *


path = "cours_script"
grammar_path = "cours_grammar"
with open(path) as f:
    script = f.read()
with open(grammar_path) as f:
    grammar = f.read()

gram = f''' {grammar} '''


registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

cpt_if_while = [-1]

funcs_arg_len = dict() #Has to be global to check if func calls respec nb args of funcs


#The code is parsed


def asm_expression(ast, parameters = None):

    if ast.data == "parenthesis": 
        return f"""
        {asm_expression(ast.children[0], parameters)}
        """
    if ast.data in  ( "variable" , "int" ):
        if ast.data == "variable":
            if parameters != None and ast.children[0].value in parameters : 
                return f"mov rax, {getRegister(ast.children[0].value , parameters )}"
            return f"mov rax, [{ast.children[0].value}]"
        else: return f"mov rax, {ast.children[0].value}"
    
    if ast.data == "function_call":
        ensure_correct_args_func(ast)
        arg_reg = ""
        arg_script = ""
        end_func_arg_script = ""
        kid_idx = 0
        for kid in ast.children[0].children[1].children:
            arg_script += asm_expression(kid, parameters)
            arg_script += f"""
            push {getRegister(kid, ast.children[0].children[1].children)}
            mov {getRegister(kid, ast.children[0].children[1].children)} , rax
            """
            end_func_arg_script += f"""
            pop {getRegister(kid, ast.children[0].children[1].children)}
            """
        
        return ";This is a function call\n" + arg_script + "\n" + arg_reg + "\n" + "call " + ast.children[0].children[0] + ";end_func_call\n" + end_func_arg_script

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
        {asm_expression(ast.children[2], parameters)}
        push rax
        {asm_expression(ast.children[0], parameters)}
        pop rbx
        {command} rax, rbx
        {boolean}
    """


    






def pp_args(ast):
    
    if ast.data == "arglist":
        arglist = ast.children
        res =  f"{arglist[0].children[0].value}"
        if len(ast.children) > 1 :
            for i in range(1 ,len(ast.children)):
                res += f" , {ast.children[i].children[0].value}"
        return res
    
def pp_command(ast, parameters):

    if ast.data == "assignment":
        lvalue = ast.children[0].value
        if lvalue in parameters : lvalue = f"(param {lvalue})"
        rvalue = pp_expression(ast.children[1], parameters)
        return f"{lvalue}  =  {rvalue}"
    if ast.data == "sequence":
        command = pp_command(ast.children[0], parameters)
        following = pp_command(ast.children[1], parameters)
        return f"{command}\n{following}"

    if ast.data == "if_else":
        test = pp_expression(ast.children[0].children[0], parameters)
        script = pp_command(ast.children[0].children[1], parameters)
        res =  f"if ( {test} ) \n  {script} "
        if len(ast.children) > 1:
            escript = pp_command(ast.children[1].children[0], parameters)
            res += f"\nelse\n  {escript} "
        return res
    
    if ast.data == "while":
        test = pp_expression(ast.children[0], parameters)
        script = pp_command(ast.children[1], parameters)
        return  f"while ( {test} ) \n  xor al , al {script} "
        

    if ast.data == "main":
        args = pp_args(ast.children[0])
        script = pp_command(ast.children[1], parameters)
        returned = pp_expression(ast.children[2].children[0], parameters)
        return f"main ( {args} )\n {script} \n return {returned}  "

    if ast.data == "function_call":
        
        return f"""
        call
        {ast.children[0].children[0]}{[kid.children[0].value  for kid in ast.children[0].children[1].children ]}
        """

    if ast.data == "return":
        
        return "return " + pp_expression(ast.children[0]) + "\n"


    return "Wrong or not implemented"


def asm_declare_vars_list(ast, vars):
    # Cette fonction dans certains cas renvoie une string, d'autre fois modif par effet de bord une liste
    if ast.data in ( 'variable' , 'int', "bin", 'assignment', 'format_str', 'format_int','function','function_call', "arglist") : return 
    if ast.data == 'declaration' :
        
        if len(ast.children) == 1:
            return ast.children[0] + ": dq 0 " 
        elif len(ast.children) == 2:
            alloc_command = "dq"
            printed_string = ast.children[1].value
            if ast.children[1].type == "STRING": 
                alloc_command = "db" 
                printed_string = str(ast.children[1])
                printed_string = printed_string.replace(r"\n",  ' ",10," ' )
                return ast.children[0] + f" : {alloc_command} " + printed_string + ", 0"
            return ast.children[0] + f" : {alloc_command} " + printed_string  
    else:
        #Appel récursif car ça n'est pas une declaration donc il faut itérer plus loin dans l'arbre
        # print(f"esle is called on {type(ast.children[0])}")
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
    if ast.data in ( 'variable' , 'int', "bin", 'assignment', 'format_str', 'format_int','function','function_call','arglist') : return 
    if ast.data == 'declaration' :
        
        if len(ast.children) == 1:
            return (ast.children[0].value, "0") 
        elif len(ast.children) == 2:
            alloc_command = "dq"
            
            if (type(ast.children[1]) == type(ast)):
                if ast.children[1].data == "parameter": printed_string = ast.children[1].children[0] 
            else: 
                printed_string = ast.children[1].value
                
                if ast.children[1].type == "STRING": 
                    alloc_command = "db" 
                    printed_string = str(ast.children[1])
                    printed_string = printed_string.replace(r"\n",  ' ",10," ' )
                    return ast.children[0] + f" : {alloc_command} " + printed_string + ", 0"
            return (ast.children[0].value, printed_string)
    else:
        for i in range(len(ast.children)):
            
            val = asm_infunc_declare_vars_list( ast.children[i] , vars )
            if val != None: vars.append(val)



def asm_declare_vars(vars : list):
    ret = ""
    for var in vars: ret += f"{var}\n"
    return ret




def asm_command(ast, parameters = None):
    
    if ast.data == "assignment":
        if ast.children[1].data == 'int':
            if parameters != None and ast.children[0] in parameters:
                return f"mov {getRegister(ast.children[0], parameters)} , " + ast.children[1].children[0].value + "\n"
            return "mov qword [" + ast.children[0] + "] , " + ast.children[1].children[0].value + "\n"

        if (ast.children[1].data == 'bin') :
            if (parameters != None) and ast.children[0].value in parameters:
                
                if ast.children[1].data == 'function_call':
                    if ast.children[1].children[0].children[0].value not in funcs_arg_len : 
                
                        raise ValueError(f'Called function {ast.children[1].children[0].children[0].value} but it was never defined !')
                    return f"""
                    {asm_expression(ast.children[1])}
                    mov {getRegister(ast.children[0].value,parameters)} , rax
                    """

                return  f"""{asm_expression(ast.children[1], parameters)}
                    mov {getRegister(ast.children[0].value, parameters)} , rax
                """
            return f"""
                    {asm_expression(ast.children[1], parameters)}
                    mov qword [{ast.children[0].value}] , rax
            """
        
        if ast.children[1].data == 'function_call':
            ensure_correct_args_func(ast.children[1])
            return f"""
            {asm_expression(ast.children[1])}
            mov qword [{ast.children[0].value}] , rax
            """

        
        
        

    if ast.data == "declaration":
        return ""
         

    if ast.data == "sequence":
        
        command = asm_command(ast.children[0], parameters)
        following = asm_command(ast.children[1], parameters)

        return f"{command}{following}"

    if ast.data == "if_else":
        test = asm_expression(ast.children[0].children[0], parameters)
        script = asm_command(ast.children[0].children[1], parameters)
        script_else = asm_command(ast.children[1].children[0], parameters)

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
        test = asm_expression(ast.children[0], parameters)
        script = asm_command(ast.children[1], parameters)
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

                if parameters != None and  ast.children[1].children[0] in parameters:
                    reg = getRegister(ast.children[1].children[0], parameters)
                    # if reg == "rdi": reg = registers[len(parameters) - 1]
                    return f"""
                    
                    push rdi
                    push rsi
                    push rax
                    xor rax, rax
                    mov rdi, asm_int_prtr
                    mov rsi, {reg}
                    call printf
                    pop rax
                    pop rsi
                    pop rdi
                    """
                return f"""
                    mov rdi, asm_int_prtr
                    mov rsi, [{ast.children[1].children[0]}]
                    xor rax, rax
                    call printf
                """
                #HERE
        else : 
            
            stret = asm_expression(ast.children[1], parameters)
            
            if ast.children[0].children[0] == "int" :
                return stret + f"""
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                """
    
    if ast.data == "function_call":
        ensure_correct_args_func(ast)
        return f"""
            {asm_expression(ast.children[0].children[0], parameters)}
        """


    if ast.data == "return":
        returned = asm_expression(ast.children[0], parameters) #will put return into rax
        
        return f"""
        {returned}
        mov rsp, rbp           
        pop rbp     
        ret
        """



    # print(f"wrong ast : {ast}")
    
    return "Wrong or not implemented"

def getRegister(arg : str , parameters : list):
    assert arg in parameters
    index = parameters.index(arg)
    if index < len(registers):    return registers[index]

def ensure_correct_args_func(ast):
    if ast.children[0].children[0].value not in funcs_arg_len : 
            raise ValueError(f'Called function {ast.children[0].children[0].value} but it was never defined !')
    nb_args = len(ast.children[0].children[1].children)
    expected_nb_args = funcs_arg_len[ast.children[0].children[0].value] 
    if  nb_args != expected_nb_args  : raise ValueError(f"Error : function {ast.children[0].children[0].value} expected {expected_nb_args} arguments but got {nb_args}" )
        

def asm_func(ast):
    func_script = ""
    for child in ast.children:
        if child.data == "function":
            
            args = child.children[1]
        
            vars = []
            asm_infunc_declare_vars_list(child.children[2], vars)
            
            if len(vars) != 0:
                var_dec = f"""
                    
                    sub rsp, {int(8*len(vars) / 16)*16 + 16}
                """
            else: var_dec = ""
            
            arg_list_to_replace = [kid.children[0].value for kid in child.children[1].children ]

            funcs_arg_len[child.children[0].value] = len(arg_list_to_replace)

            script = asm_command(child.children[2], arg_list_to_replace)
            # returned = asm_expression(child.children[3].children[0], arg_list_to_replace)
            arg_list = []
            argument_script = ""
            #init registers to replace vars in func 
            reg_index = 0

            for argument in arg_list_to_replace:
                val = argument
                arg_list.append(val)
    
            #Vars contains the list of variables that were collected by asm_infunc_declare_vars_list
            for  i in range(len(vars)):
                var_dec += f"mov qword [rbp - {8*(i+1)}],{vars[i][1]}\n" 
                script = script.replace(f"[{vars[i][0]}]", f"[rbp - {(i+1)*8}]" )

            func_script +=  f"""
            ;This is a function
            {child.children[0]}:                    ;Name of func

            push rbp
            mov rbp, rsp
            {var_dec}
            {script}    
            """      
    # print(funcs_arg_len)
    return (func_script, funcs_arg_len)
  
  
  
  
def asm_main(ast):
    for child in ast.children:

        if child.data == "main":
            decl_vars_main, init_vars_main = asm_init_vars_main(child.children[0])
            script = asm_command(child.children[1])
            returned = asm_expression(child.children[2].children[0])
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
    
    # print(f"wrong in main ast : {ast}")

    
    return "Wrong or not implemented", "Wrong or not implemented"
    



def assembly(script):
    vars = []
    l = lark.Lark(gram, start= "start")
    t = l.parse(script)
    # print(t.children[0].pretty())
    asm_script = """extern printf; e.g stdio.h
    extern atoi;
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    """

    fun_ret = asm_func(t) #Has to be put first to ensure that func calls respect nb of vars
    fun = fun_ret[0]
    fun_args = fun_ret[1]

    main_prog, init_vars_main = asm_main(t)

    asm_script += init_vars_main

    asm_declare_vars_list(t, vars)
    asm_script +=  asm_declare_vars(vars)

    asm_script += """   global main
    section .text"""
    

    if  fun != None:    
        asm_script += fun


    asm_script += main_prog
    

    with open("tuto_assembly/test.asm", "w") as f:
        f.write(asm_script)
    # os.system("./tuto_assembly/build.sh tuto_assembly/test.asm")

def run(code = script):
    assembly(code)
    os.system("./tuto_assembly/build.sh tuto_assembly/test.asm")

def pp_func(ast):
    func = f""
    for child in ast.children:
        if child.data == "function":
            script = child.children[2]
            params = [kid.children[0].value for kid in child.children[1].children ]
            
            func += f""" {child.children[0]}({[kid.children[0].value for kid in child.children[1].children ]})

            {pp_command(script, params)}
            """
            func += "\n \n"
    print(func)
    


if __name__ == '__main__':
    # l2 = lark.Lark(string,start="main")
    # tasm = l2.parse("main(x){int x ; while(x < 10 ) {x = x +1; int z = 0; }return 0 ;}")
    # # print(asm_command(tasm))
    # vars = []
    # asm_declare_vars(tasm, vars)
    # print(vars)
    assembly(script)
    
    # l = Lark(gram, start= "main")
    # t = l.parse(script)
    # pp_func(t)