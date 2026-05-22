import os
from lark import Lark

path = "cours_script"
grammar_path = "cours_grammar"
with open(path) as f:
    script = f.read()
with open(grammar_path) as f:
    grammar = f.read()

gram = f''' {grammar} '''
l = Lark(gram,start="main")

registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]


#The code is parsed

def pp_expression(ast, parameters = None):
    if ast.data == "parenthesis": return f"( {pp_expression(ast.children[0])} )"
    if ast.data in  ( "variable" , "int"  ):
        val = ast.children[0].value
        if parameters != None and val in parameters : 
            val = f"(param   {val})"
        return val
    lo = f"{pp_expression(ast.children[0], parameters)}"
    op = f"{ast.children[1].value}"
    ro = f"{pp_expression(ast.children[2], parameters)}"
    
    return lo + " " + op + " " + ro


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
        # print(ast.children[0].children[1].children)
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
            end_func_arg_script = f"""
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
    if ast.data in ( 'variable' , 'int', "bin", 'assignment', 'format_str', 'format_int','function','function_call', 'parameter') : return 
    if ast.data == 'declaration' :
        
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


def asm_infunc_declare_vars_list(ast, vars):
    if ast.data in ( 'variable' , 'int', "bin", 'assignment', 'format_str', 'format_int','function','function_call') : return 
    if ast.data == 'declaration' :
        
        print("and\n")
        if len(ast.children) == 1:
            return (ast.children[0].children[0].value, "0") 
        elif len(ast.children) == 2:
            alloc_command = "dq"
            
            print(type(ast.children[1]))
            if (type(ast.children[1]) == type(ast)):
                if ast.children[1].data == "parameter": printed_string = ast.children[1].children[0] 
            else: 
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




def asm_command(ast, parameters = None):
    
    if ast.data == "assignment":
        if ast.children[1].data == 'int':
            if parameters != None and ast.children[0] in parameters:
                return f"mov {getRegister(ast.children[0], parameters)} , " + ast.children[1].children[0].value + "\n"
            return "mov qword [" + ast.children[0] + "] , " + ast.children[1].children[0].value + "\n"

        if (ast.children[1].data == 'bin') :
            if (parameters != None) and ast.children[0].value in parameters:
                
                if ast.children[1].data == 'function_call':
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

        return f"""
        {test}
        cmp rax, 0
        jz end
        {script}
        jmp end_else
        end:
        {script_else}
        end_else:
        """
        
    if ast.data == "while":        
        test = asm_expression(ast.children[0], parameters)
        script = asm_command(ast.children[1], parameters)
        return  f"""
        while:
            {test}
            cmp rax, 0
            jz end_while
            {script}
            jmp while
        end_while:
        """

    if ast.data == "print":
        if ast.children[1].data == "variable":
            if ast.children[0].children[0] == "str":
                return f"""
                    mov rdi, {ast.children[1].children[0]}
                    call printf
                """
            elif ast.children[0].children[0] == "int" :

                if parameters != None and  ast.children[1].children[0] in parameters:
                    reg = getRegister(ast.children[1].children[0], parameters)
                    # if reg == "rdi": reg = registers[len(parameters) - 1]
                    return f"""
                    push rbx ; Dummy
                    push rdi
                    push rsi
                    push rax
                    mov rax, {reg}
                    mov rdi, asm_int_prtr
                    mov rsi, rax 
                    call printf
                    pop rax
                    pop rsi
                    pop rdi
                    pop rbx
                    """
                return f"""
                    mov rdi, asm_int_prtr
                    mov rsi, [{ast.children[1].children[0]}] 
                    call printf
                """
                #HERE
        else : 
            
            stret = asm_expression(ast.children[1], parameters)
            
            if ast.children[0].children[0] == "int" :
                return stret + f"""
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    call printf
                """


    if ast.data == "main":
        script = asm_command(ast.children[1], parameters)
        returned = asm_expression(ast.children[2].children[0], parameters)
        return f"""
        main:
        push rbp            
        mov rbp, rsp
        {script}
    
        """

    
    if ast.data == "function_call":
        
        # arg_reg = ""
        # for param in parameters :
        #     arg_reg += f"mov {getRegister(param)} , [{parameters}]"
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



    
    
    return "Wrong or not implemented"

def getRegister(arg : str , parameters : list):
    assert arg in parameters
    index = parameters.index(arg)
    if index < len(registers):    return registers[index]


def asm_func(ast):
    # print(ast)
    func_script = ""
    
    for child in ast.children:
        if child.data == "function":
            
            args = child.children[1]
        
            vars = []
            asm_infunc_declare_vars_list(child.children[2], vars)
            
            if len(vars) != 0:
                var_dec = f"""
                    push rbp
                    mov rbp, rsp
                    sub rsp, {int(8*len(vars) / 16)*16 + 16}
                """
            else: var_dec = ""
            
            arg_list_to_replace = [kid.children[0].value for kid in child.children[1].children ]

            script = asm_command(child.children[2], arg_list_to_replace)
            # returned = asm_expression(child.children[3].children[0], arg_list_to_replace)
            arg_list = []
            argument_script = ""
            #init registers to replace vars in func 
            reg_index = 0

            for argument in arg_list_to_replace:
                val = argument
                
                arg_list.append(val)
    

            for  i in range(len(vars)):
                # print("will put as rval :" ,vars[i] )
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

        
    return func_script
    



def assembly(script):
    vars = []
    l = Lark(gram, start= "main")
    t = l.parse(script)

    asm_script = """extern printf; e.g stdio.h
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    """


    asm_declare_vars_list(t, vars)
    asm_script +=  asm_declare_vars(vars)

    asm_script += """   global main
    section .text"""
    fun = asm_func(t) 
    if  fun != None:    
        asm_script += fun


    asm_script += asm_command(t)
    

    asm_script += """
    mov rdi, asm_ret_msg
    call printf
    pop rbp
    ret
    """    
    # print(asm_command(t))
    # print(t.pretty())
    print(asm_script)
    with open("tuto_assembly/test.asm", "w") as f:
        f.write(asm_script)
    os.system("./tuto_assembly/build.sh tuto_assembly/test.asm")


def pp_func(ast):
    # print(ast)
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
    # l2 = Lark(string,start="main")
    # tasm = l2.parse("main(x){int x ; while(x < 10 ) {x = x +1; int z = 0; }return 0 ;}")
    # # print(asm_command(tasm))
    # vars = []
    # asm_declare_vars(tasm, vars)
    # print(vars)
    assembly(script)
    
    # l = Lark(gram, start= "main")
    # t = l.parse(script)
    # pp_func(t)