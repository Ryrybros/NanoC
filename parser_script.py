import os
import lark
from pretty_printer_script import *



path = "cours_script.c"
grammar_path = "cours_grammar"
with open(path) as f:
    script = f.read()
with open(grammar_path) as f:
    grammar = f.read()

gram = f''' {grammar} '''

var_data_rec = ( 'parameter',   'sequence', 'if_else', 'while', "main", "start")

cpt_if_while = [-1]

main_global_vars = dict()


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
    if ast.data == "for":
        asm_declare_vars_list(ast.children[5], vars)


def asm_declare_tab(ast, vars : dict, parameters):
    if ast.data == "declaration_tab":
        type1 = asm_compare_types_expression(ast.children[0], variables_dict= variables_dict, parameters=parameters)
        type2 = asm_types_tab(ast.children[1], vars, parameters)
        if  type1 != type2 :
            raise TypeError(f"Wrong type assignment cannot assign {type2} to {type1}")  
        
        vars[ast.children[1].value] =  ast.children[0].value
        tab = ast.children[2]
        decl = f"{ast.children[1].value} : dq "
        decl += ", ".join(f"{tab.children[i]}" for i in range(len(tab.children)))
        return decl
    if ast.data in var_data_rec:
        #Appel récursif car ça n'est pas une declaration donc il faut itérer plus loin dans l'arbre
        for i in range(len(ast.children)):
            asm_declare_tab( ast.children[i] , vars, parameters)



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
    for var in vars:

        if "[" in vars[var]:

            len = vars[var][vars[var].find("[") + 1 : vars[var].find("]")]
            ret += f"""asm_static_tab_{var} times {len} dq 0
            {var} : dq 0\n"""
        else:
            ret += f"{var} : dq 0\n"
    return ret


def asm_ptr_tab(vars : list):
    ret = ""
    for var in vars:
        if "[" in vars[var]:
            ret += f"""mov rax, asm_static_tab_{var}
            mov [{var}], rax\n"""
    return ret







































##########################################Expressions###########################################

funcs_arg_len = dict() #Has to be global to check if func calls respec nb args of funcs
func_types = dict()
func_args = dict()
current_function = ["Unassigned"]


#The code is parsed

registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

def registerSaver(parameters : dict, start : bool):
    ret = ""
    push_pop = ""
    if start : push_pop = "push"
    else: push_pop = "pop"
    if start:
        ret += f"""push r11"""
        for param in registers:
            

            ret += f"""
            push {param} ; saving {param}
            """
    else:
        for param in reversed(registers):
            ret += f"""
            pop {param}
            """
        ret += f"""pop r11"""

    return ret

def getRegister(arg : str , variables_dict_len: int ,parameters : list, ind : int = None):
    # print("compare", ast)
    assert arg in parameters
    if ind == None : index = parameters.index(arg)
    else : index = ind

    if index < len(registers):    return registers[index]
    else : return f"[ rbp + {16 + (index - 6)*8} ]"


def isPointer(tipe):
    return tipe[-1] == "*"

def tabToPt(ast):
    if ast.data == "simple_tab":
        tpt = lark.Tree("expr_deref", [lark.Token("POINTER_ORDER", "*"), lark.Tree('bin', [lark.Tree('variable', [ast.children[0]]), lark.Token('OPBIN', '+'), lark.Tree('bin', [lark.Tree('int', [lark.Token('SIGNED_NUMBER', 8)]), lark.Token('OPBIN', '*'), ast.children[1]])])])
        #print(tpt.pretty())
        return tpt

    if ast.data == "tab_tab":
        tpt =  lark.Tree('expr_deref', [lark.Token('POINTER_ORDER', '*'), lark.Tree('bin', [lark.Tree('dereferencing', [tabToPt(ast.children[0])]), lark.Token('OPBIN', '+'), lark.Tree('bin', [lark.Tree('int', [lark.Token('SIGNED_NUMBER', 8)]), lark.Token('OPBIN', '*'), ast.children[1]])])])
        #print(tpt.pretty())
        return tpt

    # print("pb", ast.pretty())
    raise AssertionError("Wrong or not implemented", ast.pretty)

def asm_compare_types_expression(ast, variables_dict : dict, parameters: dict):

    if type(ast) == lark.lexer.Token: 
        if ast.value in variables_dict : return variables_dict[ast.value]
        else: return parameters[ast.value]
    if ast.data == "parenthesis": 
        return asm_compare_types_expression(ast.children[0], variables_dict= variables_dict, parameters=parameters)
    
    if ast.data in  ( "variable" , "int" ):
        if ast.data == "variable":
            
            if parameters != None and ast.children[0].value in parameters :
                return parameters[ast.children[0].value]
            

            k = ast.children[0].value
            
            if not(k in variables_dict.keys()):
                raise ValueError(f"Not defined variable {k}")
            
            return variables_dict[k]
        return "int"

    if ast.data == "function_call":
        
        return func_types[ ast.children[0].children[0].value ]
    if ast.data == "bin":
        type1 = asm_compare_types_expression(ast.children[0], variables_dict= variables_dict, parameters=parameters)
        type2 = asm_compare_types_expression(ast.children[2], variables_dict= variables_dict, parameters=parameters) 
        
        if type1 == type2 and type1 == "int":
            return type1
        elif type1 == "int" and isPointer(type2):
            return type2
        elif isPointer(type1) and type2 == "int":
            return type1
        else:
            raise TypeError(f"Wrong Type binary operation between {type1} and {type2}") 



    if ast.data == "dereferencing":
        deref_child = ast.children[0]
        if (deref_child.data == "single_deref"):
            type1 = asm_compare_types_expression(deref_child.children[1], variables_dict, parameters)
            
        
        if (deref_child.data == "expr_deref"):
            type1 = asm_compare_types_expression(deref_child.children[1], variables_dict, parameters)

        for i in range(len(deref_child.children[0].value)):
            if len(type1) <= 1 or type1[-1] != "*":
                raise TypeError(f"Wrong Type Dereferencing get type {type1[:-1]}")
            type1 = type1[:-1]

        return type1


    if ast.data == "eltab_read" or ast.data == "eltab_write":
        return asm_types_eltab(ast.children[0], variables_dict, parameters)

    if ast.data == "len":
        type_expr = asm_compare_types_expression(ast.children[0], variables_dict, parameters)
        if "[" not in type_expr:
            raise TypeError(f"Wrong Type {type_expr} not an array")
        return "int"
        

    raise AssertionError("Wrong or not implemented", ast)


def asm_types_eltab(ast, variables_dict : dict, parameters : dict):
# Vérifie d'abord si l'expression est bien un entier
    type_expr = asm_compare_types_expression(ast.children[1], variables_dict, parameters)
    if type_expr != "int" : raise TypeError(f"Wrong Type {type_expr} not an int")
    
    # Renvoie le type de l'élément du tableau
    if ast.data == "simple_tab":
        
        type_tab = asm_compare_types_expression(ast.children[0], variables_dict, parameters)
            # Type du tableau
        if "[" in type_tab:         # Tableau statique
            i = type_tab.find("[")
            j = type_tab.find("]")
            return type_tab[:i] + type_tab[j+1:]
        else:                       # Pointeur
            return type_tab[:-1]
    if ast.data == "tab_tab":   # eltab.data == "tab_tab"
        type_tab = asm_types_eltab(ast.children[0], variables_dict, parameters)
        if "[" in type_tab:         # Tableau statique
            i = type_tab.rfind("[")
            return type_tab[:i]
        else:                       # Pointeur
            return type_tab[:-1]
    raise AssertionError("Wrong or not implemented", ast)


def asm_types_tab(ast, variables_dict : dict, parameters : dict):
# type d'un tableau écrit directement
    nb_el = len(ast.children)
    if ast.data == "int_tab":
        return f"int[{nb_el}]"
    if ast.data == "var_tab":
        type1 = variables_dict[ast.children[0].value]
        for var in ast.children[1:]:
            type2 = variables_dict[var.value]
            if type2 != type1:
                raise TypeError(f"Wrong type {type2} in array of {type1}")
        return f"{type1}[{nb_el}]"
    
    raise AssertionError("Wrong or not implemented", ast)
    

def asm_expression(ast, variables_dict :dict , parameters : dict):

    if ast.data == "parenthesis": 
        return f"""
        {asm_expression(ast.children[0], variables_dict= variables_dict, parameters=parameters)}
        """
    if ast.data in  ( "variable" , "int" ):
        if ast.data == "variable":
            # assert type(variables_dict) == dict
            # assert(len(variables_dict) >= 1)
            return f"mov rax, [{ast.children[0].value}]"
        else: return f"mov rax, {ast.children[0].value}"
    
    if ast.data == "function_call":
        ensure_correct_args_func(ast,variable_parameters=variables_dict, function_param_parameters= parameters)
        arg_reg = ""
        arg_script = ""
        start_arg_script = ""
        end_arg_script = ""
        end_func_arg_script = ""
        kid_idx = 0


        index = 0
        for kid in ast.children[0].children[1].children:
            
            if index < 6:

                #Pushes all registers to ensure that they are not lost after func call
                arg_script += asm_expression(kid, variables_dict= variables_dict, parameters=parameters)
                
                start_arg_script += f"""
                push {getRegister(kid, variables_dict_len= len(variables_dict), parameters=ast.children[0].children[1].children, ind=index)}
                
                """

                arg_script += f"""
                push rax

                """
            else:
                arg_script = f"""
                {asm_expression(kid, variables_dict= variables_dict, parameters=parameters)}
                push rax
                """ + arg_script
            
            
            index += 1
        index -= 1

        arg_script = """;start arg scipt 
        """  + arg_script + "; here for arg"

        index_rev = index
        for kid in ast.children[0].children[1].children[::-1]:
            
            if index_rev < 6:
                
                end_arg_script += f"""
                pop {getRegister(kid, variables_dict_len= len(variables_dict), parameters=ast.children[0].children[1].children, ind=index_rev)}
                """

            
            index_rev -= 1


        
        if index >= 6:
            end_func_arg_script += f""" 
            add rsp, {8*(index - 5)} 
            """
        for kid in  reversed( ast.children[0].children[1].children ):
            if index < 6:
                end_func_arg_script += f"""
                pop {getRegister(kid, variables_dict_len=len(variables_dict), parameters=ast.children[0].children[1].children, ind=index)}
                """
            index -= 1
        return ";This is a function call\n" + start_arg_script + "\n" + arg_script + "\n" + arg_reg + "\n" + end_arg_script + "\n" "call " + ast.children[0].children[0] + ";end_func_call\n" + end_func_arg_script

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

        if op == "&&":
            command = "and"

        if ast.data == "dereferencing":
            None

        if command == "div":
            return f"""
            {asm_expression(ast.children[2], variables_dict= variables_dict, parameters=parameters)}
            push rax
            {asm_expression(ast.children[0],  variables_dict=variables_dict, parameters=parameters)}
            pop rbx
            push rdx
            xor rdx, rdx
            div rbx
            pop rdx
            """
        return f""" 
            {asm_expression(ast.children[2], variables_dict= variables_dict, parameters=parameters)}
            push rax
            {asm_expression(ast.children[0],  variables_dict=variables_dict, parameters=parameters)}
            pop rbx
            {command} rax, rbx
            {boolean}
        """

    if ast.data == "dereferencing":
        return asm_dereferencing_value(ast.children[0], variables_dict, parameters)


    if ast.data == "eltab_read":
        tpt = tabToPt(ast.children[0])
        asm_instruct = asm_dereferencing_value(tpt, variables_dict, parameters)
        return asm_instruct

    if ast.data == "len":
        type_tab = asm_compare_types_expression(ast.children[0], variables_dict, parameters)
        l = type_tab[type_tab.find("[")+1 : type_tab.find("]")]
        return f"mov rax, {l}"



    raise AssertionError("Wrong or not implemented", ast)

def asm_lexpression(ast, variable_dict : dict, parameters :  dict):
    # calcule des expressions qui vont être assignées à gauche
    # The result is put in rax
    if ast.data == "dereferencing":
        # print("left epxr, dere", asm_assign_dereferencing(ast, variable_dict, parameters)+";")
        # print(asm_assign_dereferencing(ast.children[0], variable_dict, parameters), ast.pretty())
        return asm_assign_dereferencing(ast.children[0], variable_dict, parameters)

    if ast.data == "variable":
        return f"mov [{ast.children[0].value}] , rax"
    
    if ast.data == "eltab_write":
        tpt = tabToPt(ast.children[0])
        # print("etlab_read in expr\n", tpt.pretty())
        # print(asm_instruct)
        return asm_assign_dereferencing(tpt, variable_dict, parameters)

        
        
    raise AssertionError("Wrong or not implemented", ast)




def ensure_correct_args_func(ast, variable_parameters : dict, function_param_parameters : dict):
    # print(func_args)
    func_name = ast.children[0].children[0]
    
    
    #ast.children[0].children[1].children[0].data
    
    if ast.children[0].children[0].value not in funcs_arg_len : 
            raise ValueError(f'Called function {ast.children[0].children[0].value} but it was never defined !')
    nb_args = len(ast.children[0].children[1].children)
    expected_nb_args = funcs_arg_len[ast.children[0].children[0].value] 
    if  nb_args != expected_nb_args  : raise ValueError(f"Error : function {ast.children[0].children[0].value} expected {expected_nb_args} arguments but got {nb_args}" )

    i = 0
    # print(len( ast.children[0].children[1].children ))
    for arg in ast.children[0].children[1].children:

        positional_arg = list(func_args[func_name].keys())[i]
        if arg.data == "int" and func_args[func_name][positional_arg] != "int" : raise TypeError(f"Wrong argument type, expected {func_args[func_name][positional_arg]} got int")
        
        
        if arg.data == "variable" :
        
            if variable_parameters != None and arg.children[0].value in variable_parameters:
                if func_args[func_name][positional_arg] != variable_parameters[arg.children[0].value] : raise TypeError(f"Wrong argument type, expected {func_args[func_name][positional_arg]} got {variable_parameters[arg.children[0].value]}") 
        
            if function_param_parameters != None and arg.children[0].value in function_param_parameters:
                if func_args[func_name][positional_arg] != function_param_parameters[arg.children[0].value] : raise TypeError(f"Wrong argument type, expected {func_args[func_name][positional_arg]} got {function_param_parameters[arg.children[0].value]}") 
                # if func_args[list(func_args.keys())[i]]
        i = i + 1
    
        
# derefencer((t+3), 1)
# q = *(t+3)
# ...
# derefencer(q + 4*64)

# derefencer(t+3, 1)

# rax = *(t+E)

# ... 

# derefencer((reg + 4), 1)

# ...
# rax = *(rax + 4) = *(*(t+3)+4)

# pt_to_derefencer()

# convert tab.ast to pt.ast




def asm_assign_dereferencing(ast, variables_dict, parameters):
    # accede a l'adresse du dereferencement
    # print("asm_assign", ast)
    n = len(ast.children[0].value)

    # Met dans rax le contenu
    deref = ""
    for i in range(n-1):
        deref += "    mov rax, [rax]\n"
    if (ast.data == "single_deref"):
        return f"""       
    mov rax, [{ast.children[1].value}]     
{deref}"""
    if (ast.data == "expr_deref"):
        return f"""       
    {asm_expression(ast.children[1], variables_dict, parameters)}     
{deref}"""

    raise AssertionError("dereferencing not matched")

def asm_dereferencing_value(ast, variables_dict, parameters):
    # accede au contenue du dereferencement
    # print("asm_value", ast)

    return f""" {asm_assign_dereferencing(ast, variables_dict, parameters)}      
    mov rax, [rax]"""

def asm_declaration_pointeur(ast, variables_dict):
    assert(len(ast.children) == 2)
    return f"{ast.children[1].value} : dq 0\n"



def asm_allocation(ast, variables_dict, parameters):
    assert(len(ast.children) == 2)
    return f"""
    {asm_expression(ast.children[1], variables_dict, parameters)}
    {registerSaver(parameters,True)}
    mov rdi, rax
    call malloc
    {registerSaver(parameters,False)}
    """



def asm_adressing(ast):
    return f"""mov rax, QWORD {ast.value}"""












##########################################End_Expressions###########################################













































def asm_command_assign(assign_catego, lexpr, rexpr):
    # a partir d'une left expression calculée avec asm_lexpression et une right expression calculée avec asm_expression, assigne les deux selon le type d'assignement
    # Suppose that the result of lexpr and rexpr are put in rax
    if assign_catego == "variable":
        # print(f"""
        #     {rexpr}
        #     {lexpr}
        #     """)
        return f"""
            {rexpr}
            {lexpr}
            """

    if assign_catego in ("dereferencing", "eltab_write") :
        return f"""
            {lexpr}
            push rax
            {rexpr}
            pop rbx
            mov [rbx] , rax
            """


    
    

    raise AssertionError(f"Wrong or not implemented : {assign_catego}")



def asm_command(ast, variables_dict : dict , parameters : dict):
    
    
    if ast.data == "assignment":
        
        type1 = asm_compare_types_expression(ast.children[0], variables_dict= variables_dict, parameters=parameters)
        type2 = asm_compare_types_expression(ast.children[1], variables_dict= variables_dict, parameters= parameters) 
        if  type1 != type2 :

            raise TypeError(f"Wrong type assignment cannot assign {type2} to {type1}")  
        

        rexpr = asm_expression(ast.children[1], variables_dict= variables_dict, parameters= parameters)

        if ast.children[0].data == "variable":            

            # a regrouper pour pouvoir generaliser au leftexpression

        
            lexpr = asm_lexpression(ast.children[0], variables_dict, parameters)
            return asm_command_assign(ast.children[0].data, lexpr, rexpr)
        
            if ast.children[1].data == 'function_call':
                ensure_correct_args_func(ast.children[1], variable_parameters=variables_dict , function_param_parameters= parameters)
                return f"""
                {rexpr}
                mov qword [{ast.children[0].value}] , rax
                """

        if ast.children[0].data == "dereferencing":
            # print("leftderef", ast.children[0])
            c = ast.children[0]
            lexpr = asm_lexpression(c, variables_dict, parameters)
            return asm_command_assign(c.data, lexpr, rexpr)

        if ast.children[0].data == "eltab_write":
            c = ast.children[0]
            lexpr = asm_lexpression(c, variables_dict, parameters)
            return asm_command_assign("dereferencing", lexpr, rexpr)
            

    if ast.data == "addressing":
        print(variables_dict)
        type1 = asm_compare_types_expression(ast.children[0], variables_dict, parameters)
        if variables_dict != None and  ast.children[1].value in variables_dict : type2 = variables_dict[ast.children[1].value]+"*"
        if parameters != None and ast.children[1].value in parameters : type2 = parameters[ast.children[1].value]+"*"

        type2 = asm_compare_types_expression(ast.children[1],variables_dict,parameters)+"*"
        

        if type1 != type2: raise TypeError(f"Wrong type at line {ast.line} assignment cannot assign  {type2} to {type1}") 
        c = ast.children[0]
        lexpr = asm_lexpression(c, variables_dict, parameters)
        # print(asm_command_assign(c.data, lexpr, asm_adressing(ast.children[1])))
        return asm_command_assign(c.data, lexpr, asm_adressing(ast.children[1]))


    if ast.data == "allocation":
        # In malloc, the number passed to malloc is the number of bytes
        # print(ast)
        type1 = asm_compare_types_expression(ast.children[0], variables_dict, parameters)
        type2 = asm_compare_types_expression(ast.children[1], variables_dict, parameters)
         
        if type2 != "int":
            raise TypeError(f"{type2} n'est pas de type entier")

        
        if not isPointer(type1):
            raise TypeError(f"{type1} n'est pas de type pointeur")

        rexpr = asm_allocation(ast, variables_dict, parameters)
        # print(rexpr)
        c = ast.children[0]
        lexpr = asm_lexpression(c, variables_dict, parameters)
        # print(asm_command_assign(c.data, lexpr, rexpr))
        return asm_command_assign(c.data, lexpr, rexpr)
    

    if ast.data == "assignment_tab":
        type1 = asm_compare_types_expression(ast.children[0], variables_dict= variables_dict, parameters=parameters)
        type2 = asm_types_tab(ast.children[1], variables_dict, parameters)
        if  type1 != type2 :
            raise TypeError(f"Wrong type assignment cannot assign {type2} to {type1}")  
        
        l = ast.children[0]

        # Calcul de l'expression de droite
        if l.data == "dereferencing":
            lexpr = asm_assign_dereferencing(l.children[0], variables_dict, parameters)

        if l.data == "variable":
            lexpr = f"mov rax, {l.children[0].value}\n"
    
        if l.data == "eltab_write":
            tpt = tabToPt(l.children[0])
            lexpr = asm_assign_dereferencing(tpt, variables_dict, parameters)

        lexpr += "mov rax, [rax]"
        tab = ast.children[1]
        res = ""

        if tab.data == "var_tab":
            for i in range(len(tab.children)):
                val = asm_expression(tab.children[i], variables_dict, parameters)
                res += f"""{lexpr}
                mov rax, rax + 8*{i}
                push rax
                {val}
                pop rbx
                mov [rbx], rax
                \n"""
            return res
        
        if tab.data == "int_tab":
            for i in range(len(tab.children)):
                val = tab.children[i].value
                res += f"""{lexpr}
                add rax, 8*{i}
                push rax
                mov rax, {val}
                pop rbx
                mov [rbx], rax
                \n"""
            return res



    if ast.data == "comment":
        return ""        

    if ast.data == "declaration":
        
        if "int[" in ast.children[0]:
            if current_function[0] != "main": raise ValueError("Cannot initialize a static tab in function other than main")

        return ""

    if ast.data == "sequence":

        command = asm_command(ast.children[0], variables_dict=variables_dict , parameters= parameters)
        following = asm_command(ast.children[1], variables_dict= variables_dict,  parameters= parameters)

        return f"{command}{following}"

    if ast.data == "if_else":
        test = asm_expression(ast.children[0].children[0], variables_dict=variables_dict, parameters= parameters)
        script = asm_command(ast.children[0].children[1], variables_dict=variables_dict,  parameters= parameters)

        script_else = asm_command(ast.children[1].children[0], variables_dict=variables_dict,  parameters= parameters)

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
        test = asm_expression(ast.children[0], variables_dict=variables_dict, parameters= parameters)
        script = asm_command(ast.children[1], variables_dict=variables_dict,  parameters=  parameters)
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
        #Debug prints
        
        

        if type(ast.children[0]) == lark.lexer.Token:
            
            if ast.children[0].type == "STRING" :
                
                string = ast.children[0].value

                if string[1:-1] == "endl" :
                    allocation = f"""
                    mov rax, 0x0A
                    push rax 
                    """
                    chunks = [string]
                else:
                    offset = len(string) % 8
                    chunks = [string[1:-1][i:i+8] for i in range(0, len(string), 8)]
                    
                    allocation = ""
                    
                    for chunk in chunks[::-1]:
                        chunk = chunk[::-1]
                        
                        allocation += f"""

                        mov rax, 0x{chunk.encode().hex().zfill(16).upper()}
                        push rax 

                        """
                return  f"""
                    
                    

                    mov rax, 0x00
                    push rax


                    {allocation}
                    mov rax, rsp
                    {registerSaver(parameters,True)}

                    push rax
                    mov rdi, rax
                    xor rax, rax
                    call printf
                    pop rax
                    {registerSaver(parameters,False)}
                    
                    add rsp, {len(chunks)*8 + 8}
                """

            
        
    

        if ast.children[1].data == "variable":
            if ast.children[0].children[0] == "str":
                return f"""
                    mov rdi, {ast.children[1].children[0]}
                    xor rax, rax
                    call printf
                """
            elif ast.children[0].children[0] == "int" :

                return f"""
                    mov rbx, [{ast.children[1].children[0]}]
                    {registerSaver(parameters,True)}
                    push rax
                    mov rdi, asm_int_prtr
                    mov rsi, rbx
                    xor rax, rax
                    call printf
                    pop rax

                    {registerSaver(parameters,False)}
                """
                #HERE
        else : 
            
            stret = asm_expression(ast.children[1], variables_dict=variables_dict, parameters= parameters)
            
            if ast.children[0].children[0] == "int" :
                return stret + f"""
                    {registerSaver(parameters,True)}
                    push rax
                    mov rdi, asm_int_prtr
                    mov rsi, rax
                    xor rax, rax
                    call printf
                    pop rax
                    {registerSaver(parameters,False)}

                """
            
            #Debug
    
    if ast.data == "function_call":
        
        ensure_correct_args_func(ast, variable_parameters=variables_dict, function_param_parameters=parameters)
        
        return f"""
            {asm_expression(ast, variables_dict=variables_dict ,parameters= parameters)}
        """


    if ast.data == "return":
        returned = asm_expression(ast.children[0], variables_dict=variables_dict, parameters=parameters) #will put return into rax
        ret_type = asm_compare_types_expression(ast.children[0], variables_dict,parameters)
        func_type = func_types[current_function[0]]
        if func_type != ret_type and func_type != "void" :
            raise TypeError(f"Wrong returned type for function {current_function[0]}, expected {func_type} and found {ret_type}")
        return f"""
        {returned}
        mov rsp, rbp           
        pop rbp     
        ret
        """
    

    if ast.data == 'for':
        #print(ast.pretty())
        ind = ast.children[0].value
        temp_var_dict = variables_dict
        temp_var_dict[f"{ind}"] = "int"
        if ast.children[2] != ind or ast.children[4] != ind:
            raise ValueError(f"{ind}, {ast.children[2]} et {ast.children[4]} n'ont pas le même nom")
        type_expr1 = asm_compare_types_expression(ast.children[1], temp_var_dict, parameters)
        type_expr2 = asm_compare_types_expression(ast.children[3], temp_var_dict, parameters)
        if type_expr1 != "int":
            raise TypeError(f"{type_expr1} n'est pas de type entier")
        if type_expr2 != "int":
            raise TypeError(f"{type_expr2} n'est pas de type entier")
        
        init = asm_expression(ast.children[1], temp_var_dict, parameters)
        end = asm_expression(ast.children[3], temp_var_dict, parameters)

        command = asm_command(ast.children[5], temp_var_dict, parameters)
        command = command.replace(f"[asm_temporary_var_{ind}]", "r11")
        command = command.replace(f"[{ind}]", "r11")

        cpt_if_while[0] += 1

        res = f"""{init}
        mov r11, rax
        for_{cpt_if_while[0]}:
        {end}
        push rax
        mov rax, r11
        pop rbx
        cmp rax, rbx
        jge end_for_{cpt_if_while[0]}

        {command}

        mov rax, 1
        push rax
        mov rax, r11
        pop rbx
        add rax, rbx
        mov r11, rax
        
        jmp for_{cpt_if_while[0]}
        end_for_{cpt_if_while[0]}:
        """

        return res

    raise AssertionError("Wrong or not implemented", ast)

def asm_ensure_return(ast):
    sub_scopes = ["if_else"]
    sub_return = False
    root_return = False
    # print(f" the tree \n {ast.pretty()} \n ")
    if ast.data == "return": return True

    if ast.data in sub_scopes:

        sub_return =  asm_ensure_return(ast.children[0].children[1]) and asm_ensure_return(ast.children[1].children[0])

    if ast.data in var_data_rec:
        root_return =  asm_ensure_return(ast.children[0]) or asm_ensure_return(ast.children[1]) 
    
    return sub_return or root_return

def asm_func(ast):
    func_script = ""
    
    #We first get the function signature, before the script 

    for child in ast.children:
        if child.data == "function":
            func_types[child.children[1].value] = child.children[0].value     

            arg_list_to_replace = [kid.children[1].value for kid in child.children[2].children ]

            funcs_arg_len[child.children[1].value] = len(arg_list_to_replace)




    for child in ast.children:
        if child.data == "function":
            func_name = child.children[1].value
            current_function[0] = func_name
            
            if not asm_ensure_return(child.children[3]) : raise TypeError(f"No return in at least one branch of function {func_name} of type {func_types[func_name]} if the type is void add return 0 to declare end of the function ")

            func_args[func_name] = dict()
            child_list = child.children[1:] 
            args = child_list[1]
            for kid in args.children:    
                func_args[func_name][kid.children[1].value] = kid.children[0].value
            vars = dict()
            asm_declare_vars_list(child_list[2], vars)
            
            if len(vars) != 0 or max( len(arg_list_to_replace) - 6, 0) != 0:
                var_dec = f"""
                    ; function args > nb_registers = {max( len(arg_list_to_replace) - 6, 0)}
                    sub rsp, {int( 8*( ( len(vars) + max( len(arg_list_to_replace), 0) ) / 16))*16  + 16}
                """
            else: var_dec = ""
            
            arg_list_to_replace = [kid.children[1].value for kid in child_list[1].children ]
            arg_list_to_replace_types = [kid.children[0].value for kid in child_list[1].children ]
        

            parameters_to_replace = dict()
            for i in range(len(arg_list_to_replace )):
                parameters_to_replace[arg_list_to_replace[i]] = arg_list_to_replace_types[i]

            funcs_arg_len[child_list[0].value] = len(arg_list_to_replace)
            

            script = asm_command(child_list[2], variables_dict= vars, parameters=parameters_to_replace)
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
                #BACKHERE
                
                var_dec += f"mov qword [rbp - {8*(i+1 + len(arg_list_to_replace))}],0\n" 
                script = script.replace(f"[{key}]", f"[rbp - {(i+1 + len(arg_list_to_replace))*8}]" )
                script = script.replace(f"mov rax, QWORD {key}", f"lea rax, [rbp - {(i+1 + len(arg_list_to_replace))*8}]" )
                i = i + 1

            i = 0
            for key in arg_list_to_replace:
                # print( f"replacing {key} with {getRegister(key, 0 ,arg_list_to_replace)}")
                script = script.replace(f"[{key}]", getRegister(key, 0 ,arg_list_to_replace))
                script = script.replace(f"mov rax, QWORD {key}", f"lea rax, [rbp - {(i+1 + len(arg_list_to_replace))*8}]" )
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
            current_function[0] = "main"


            decl_vars_main, init_vars_main = asm_init_vars_main(child.children[0])
            ptr_tab = asm_ptr_tab(variables_dict)
            script = asm_command(child.children[1], variables_dict= variables_dict, parameters= decl_vars_main)
            returned = asm_expression(child.children[2].children[0], variables_dict= variables_dict, parameters= decl_vars_main)
            # Ignore completement le returned
            return f"""
            main:
            push rbp            
            mov rbp, rsp
            mov [argv], rsi

            {ptr_tab}

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
    # print(t)
    
    asm_script = """extern printf; e.g stdio.h
    extern atoi
    extern malloc
    section .data
    asm_ret_msg: db 10,"Program executed successfully." ,10 , 10, 0
    asm_int_prtr : db "%d" , 0
    argv : dq 0
    """

    fun_ret = asm_func(t) #Has to be put first to ensure that func calls respect nb of vars
    fun = fun_ret[0]
    fun_args = fun_ret[1]

    asm_declare_vars_list(t, vars)

    main_global_vars = vars

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
    
    
    # l = Lark(gram, start= "main")
    # t = l.parse(script)
    # pp_func(t)