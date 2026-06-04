import os
import lark
from pretty_printer_script import *



path = "cours_script"
grammar_path = "cours_grammar"
with open(path) as f:
    script = f.read()
with open(grammar_path) as f:
    grammar = f.read()

gram = f''' {grammar} '''

var_data_rec = ( 'parameter',   'sequence', 'if_else', 'while',  "main", "start")

cpt_if_while = [-1]



def asm_declare_vars_list(ast, vars : dict):
    # Cette fonction dans certains cas renvoie une string, d'autre fois modif par effet de bord une liste
    # if ast.data in ignore_data : return 
    if ast.data == 'declaration' :
        

        vars[ast.children[1].value] =  ast.children[0].value  
        return
    if ast.data in var_data_rec:
        #Appel récursif car ça n'est pas une declaration donc il faut itérer plus loin dans l'arbre
        
        
        for i in range(len(ast.children)):
            asm_declare_vars_list( ast.children[i] , vars )
            



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




def asm_declare_vars(vars : list):
    ret = ""
    for var in vars: ret += f"{var[0]} : dq 0\n"
    return ret











































##########################################Expressions###########################################

funcs_arg_len = dict() #Has to be global to check if func calls respec nb args of funcs
func_types = dict()

#The code is parsed

registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]


def getRegister(arg : str , parameters : list):
    assert arg in parameters
    index = parameters.index(arg)
    
    if index < len(registers):    return registers[index]

def asm_compare_types_expression(ast, variables_dict : dict):
    if ast.data == "parenthesis": 
        return asm_compare_types_expression(ast.children[0], variables_dict= variables_dict, parameters=parameters)
    
    if ast.data in  ( "variable" , "int" ):
        if ast.data == "variable":
            # print(ast.children[0])
            assert type(variables_dict) == dict
            assert(len(variables_dict) >= 1)

            return variables_dict[ast.children[0].value]
        return "int"

    if ast.data == "function_call":
        ensure_correct_args_func(ast)
        arg_reg = ""
        arg_script = ""
        end_func_arg_script = ""
        kid_idx = 0
        for kid in ast.children[0].children[1].children:
            arg_script += asm_expression(kid, variables_dict= variables_dict)
            arg_script += f"""
            push {getRegister(kid, ast.children[0].children[1].children)}
            mov {getRegister(kid, ast.children[0].children[1].children)} , rax
            """
            end_func_arg_script += f"""
            pop {getRegister(kid, ast.children[0].children[1].children)}
            """
        
        return ";This is a function call\n" + arg_script + "\n" + arg_reg + "\n" + "call " + ast.children[0].children[0] + ";end_func_call\n" + end_func_arg_script

    if ast.data == "bin":
        type1 = asm_compare_types_expression(ast.children[0], variables_dict= variables_dict)
        type2 = asm_compare_types_expression(ast.children[2], variables_dict= variables_dict) 
        if type1 != type2  : raise TypeError(f"Wrong Type binary operation between {type1} and {type2}") 
        
        return type1
    if ast.data == "dereferencing":
        return "dereferencing"

    # if ast.data == "nullptr":
    #     return asm_dereferencing(ast)

    if ast.data == "eltab":
        eltab = ast.children[0]
        # Vérifie d'abord si l'expression est bien un entier
        type_expr = asm_compare_types_expression(eltab.children[1], variables_dict=variables_dict)
        if type_expr != "int" : raise TypeError(f"Wrong Type {type_expr} not an int")
        
        # Renvoie le type de l'élément du tableau
        if eltab.data == "simple_tab":
            type_tab = variables_dict[ast.children[0].value]    # Type du tableau
        else:   # eltab.data == "tab_tab"
            type_tab = asm_compare_types_expression(eltab.children[0], variables_dict=variables_dict)   # Mais eltab n'est pas une expression...
        return type_tab[:-3]    # Type de l'élément


    raise AssertionError("Wrong or not implemented", ast)


def asm_expression(ast, variables_dict :dict , parameters = None, parameters_types = None):

    if ast.data == "parenthesis": 
        return f"""
        {asm_expression(ast.children[0], variables_dict= variables_dict, parameters=parameters)}
        """
    if ast.data in  ( "variable" , "int" ):
        if ast.data == "variable":
            # print(ast.children[0])
            assert type(variables_dict) == dict
            assert(len(variables_dict) >= 1)
            if parameters != None and ast.children[0].value in parameters : 
                return f"mov rax, {getRegister(ast.children[0].value , variables_dict = variables_dict, parameters=parameters )}"
            return f"mov rax, [{ast.children[0].value}]"
        else: return f"mov rax, {ast.children[0].value}"
    
    if ast.data == "function_call":
        ensure_correct_args_func(ast)
        arg_reg = ""
        arg_script = ""
        end_func_arg_script = ""
        kid_idx = 0
        for kid in ast.children[0].children[1].children:
            arg_script += asm_expression(kid, variables_dict= variables_dict, parameters=parameters)
            arg_script += f"""
            push {getRegister(kid, ast.children[0].children[1].children)}
            mov {getRegister(kid, ast.children[0].children[1].children)} , rax
            """
            end_func_arg_script += f"""
            pop {getRegister(kid, ast.children[0].children[1].children)}
            """
        
        return ";This is a function call\n" + arg_script + "\n" + arg_reg + "\n" + "call " + ast.children[0].children[0] + ";end_func_call\n" + end_func_arg_script

    if ast.data == "bin":
        
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

        if ast.data == "dereferencing":
            None

        return f""" 
            {asm_expression(ast.children[2], variables_dict= variables_dict, parameters=parameters)}
            push rax
            {asm_expression(ast.children[0],  variables_dict=variables_dict, parameters=parameters)}
            pop rbx
            {command} rax, rbx
            {boolean}
        """

    if ast.data == "dereferencing":
        return asm_dereferencing_value(ast)

    # if ast.data == "nullptr":
    #     return asm_dereferencing(ast)

    raise AssertionError("Wrong or not implemented", ast)



def ensure_correct_args_func(ast):
    if ast.children[0].children[0].value not in funcs_arg_len : 
            raise ValueError(f'Called function {ast.children[0].children[0].value} but it was never defined !')
    nb_args = len(ast.children[0].children[1].children)
    expected_nb_args = funcs_arg_len[ast.children[0].children[0].value] 
    if  nb_args != expected_nb_args  : raise ValueError(f"Error : function {ast.children[0].children[0].value} expected {expected_nb_args} arguments but got {nb_args}" )
        


def asm_assign_dereferencing(ast):
    # accede a l'adresse du dereferencement
    n = len(ast.children[0].children[0].value)
    
    # Met dans rax le contenu
    deref = ""
    for i in range(n-1):
        deref += "    mov rax, [rax]\n"
    if (ast.children[0].data == "single_deref"):
        return f"""       
    mov rax, [{ast.children[0].children[1].value}]     
{deref}"""
    if (ast.children[0].data == "expr_deref"):
        return f"""       
    {asm_expression(ast.children[0].children[1])}     
{deref}"""

    raise AssertionError("dereferencing not matched")

def asm_dereferencing_value(ast):
    # accede au contenue du dereferencement
    return f""" {asm_assign_dereferencing(ast)}      
    mov rax, [rax]"""

def asm_declaration_pointeur(ast):
    assert(len(ast.children) == 2)
    return f"{ast.children[1].value} : dq 0\n"

def asm_adressing(ast):
    return f"""       
    mov rax, QWORD {ast.children[1].value}
    mov [{ast.children[0].children[0].value}], rax
"""

# def asm_dereferencing(ast):
#     return f"""            
#     {asm_contenu(ast.children[0])}
# """















##########################################End_Expressions###########################################















































def asm_command(ast, variables_dict : dict() , parameters : list(), parameters_types = None):
    
    if ast.data == "assignment":
        type1 = asm_compare_types_expression(ast.children[0], variables_dict= variables_dict)
        type2 = asm_compare_types_expression(ast.children[1], variables_dict= variables_dict) 
        if  type1 != type2 : raise TypeError(f"Wrong type assignment canoot assign {type2} to {type1}")  
        

        if ast.children[0].data == "variable":            

            if (parameters != None) and ast.children[0].children[0].value in parameters:
                
                if ast.children[1].data == 'function_call' and ast.children[1].children[0].children[0].value not in funcs_arg_len : 
                    raise ValueError(f'Called function {ast.children[1].children[0].children[0].value} but it was never defined !')
                    asm_compare_types_expression(ast.children[1])
                return  f"""{asm_expression(ast.children[1], variables_dict= variables_dict , parameters= parameters)}
                    mov {getRegister(ast.children[0].children[0].value, variables_dict = variables_dict, parameters=parameters)} , rax
                """
            else: 
                asm_compare_types_expression(ast.children[1], variables_dict= variables_dict)
                return f"""
                    {asm_expression(ast.children[1], variables_dict= variables_dict, parameters= parameters)}
                    mov qword [{ast.children[0].children[0].value}] , rax
                """
            
            if ast.children[1].data == 'function_call':
                ensure_correct_args_func(ast.children[1])
                return f"""
                {asm_expression(ast.children[1])}
                mov qword [{ast.children[0].value}] , rax
                """

            

    if ast.data == "addressing":
        return asm_adressing(ast) 
        
        

    if ast.data == "declaration":
        return ""
         

    if ast.data == "sequence":
        
        command = asm_command(ast.children[0], variables_dict=variables_dict , parameters= parameters)
        following = asm_command(ast.children[1], variables_dict= variables_dict,  parameters= parameters)

        return f"{command}{following}"

    if ast.data == "if_else":
        test = asm_expression(ast.children[0].children[0], parameters= parameters)
        script = asm_command(ast.children[0].children[1], parameters= parameters)
        script_else = asm_command(ast.children[1].children[0], parameters= parameters)

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
        test = asm_expression(ast.children[0], parameters= parameters)
        script = asm_command(ast.children[1], parameters=  parameters)
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
                    reg = getRegister(ast.children[1].children[0], variables_dict = variables_dict, parameters= parameters)
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
            
            stret = asm_expression(ast.children[1], parameters= parameters)
            
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
            {asm_expression(ast, parameters= parameters)}
        """


    if ast.data == "return":
        returned = asm_expression(ast.children[0], variables_dict=variables_dict, parameters=parameters) #will put return into rax
        
        return f"""
        {returned}
        mov rsp, rbp           
        pop rbp     
        ret
        """



    
    raise AssertionError("Wrong or not implemented", ast)


# def ensure_correct_args_func(ast):
#     if ast.children[0].children[0].value not in funcs_arg_len : 
#             raise ValueError(f'Called function {ast.children[0].children[0].value} but it was never defined !')
#     nb_args = len(ast.children[0].children[1].children)
#     expected_nb_args = funcs_arg_len[ast.children[0].children[0].value] 
#     if  nb_args != expected_nb_args  : raise ValueError(f"Error : function {ast.children[0].children[0].value} expected {expected_nb_args} arguments but got {nb_args}" )
        

def asm_func(ast):
    func_script = ""
    
    for child in ast.children:
        if child.data == "function":
            func_types[child.children[1].value] = child.children[0].value
            child_list = child.children[1:] 
            args = child_list[1]
        
            vars = dict()
            asm_declare_vars_list(child_list[2], vars)
            
            if len(vars) != 0:
                var_dec = f"""
                    
                    sub rsp, {int(8*len(vars) / 16)*16 + 16}
                """
            else: var_dec = ""
            
            arg_list_to_replace = [kid.children[1].value for kid in child_list[1].children ]
            arg_list_to_replace_types = [kid.children[0].value for kid in child_list[1].children ]

            funcs_arg_len[child_list[0].value] = len(arg_list_to_replace)


            script = asm_command(child_list[2], variables_dict= vars, parameters=arg_list_to_replace)
            # returned = asm_expression(child_list[3].children[0], arg_list_to_replace)
            arg_list = []
            argument_script = ""
            #init registers to replace vars in func 
            reg_index = 0

            for argument in arg_list_to_replace:
                val = argument
                arg_list.append(val)
    
            #Vars contains the list of variables that were collected by asm_infunc_declare_vars_list
            i = 0
            for key in vars:
                
                var_dec += f"mov qword [rbp - {8*(i+1)}],0\n" 
                script = script.replace(f"[{key}]", f"[rbp - {(i+1)*8}]" )
                i = i + 1

            func_script +=  f"""
            ;This is a function
            {child_list[0]}:                    ;Name of func

            push rbp
            mov rbp, rsp
            {var_dec}
            {script}    
            """      
    
    return (func_script, funcs_arg_len)
  
  
  
  
def asm_main(ast ,variables_dict : dict()):
    for child in ast.children:

        if child.data == "main":
            decl_vars_main, init_vars_main = asm_init_vars_main(child.children[0])
            script = asm_command(child.children[1], variables_dict= variables_dict, parameters= decl_vars_main)
            returned = asm_expression(child.children[2].children[0], variables_dict= variables_dict, parameters= decl_vars_main)
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
    
    
    raise AssertionError("Wrong or not implemented", ast)
    



def assembly(script):
    vars = dict()
    l = lark.Lark(gram, start= "start")
    t = l.parse(script)
    # print("assembly", t.pretty())
    
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

    asm_declare_vars_list(t, vars)

    main_prog, init_vars_main = asm_main(t, vars)

    asm_script += init_vars_main

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







if __name__ == '__main__':
    # l2 = lark.Lark(string,start="main")
    # tasm = l2.parse("main(x){int x ; while(x < 10 ) {x = x +1; int z = 0; }return 0 ;}")
    # # print(asm_command(tasm))
    # vars = []
    # asm_declare_vars(tasm, vars)
    # print(vars)
    assembly(script)
    print(func_types)
    
    # l = Lark(gram, start= "main")
    # t = l.parse(script)
    # pp_func(t)