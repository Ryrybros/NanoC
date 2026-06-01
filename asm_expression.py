funcs_arg_len = dict() #Has to be global to check if func calls respec nb args of funcs


#The code is parsed

def get_funcs_arg_len():
    return funcs_arg_len

def set_funcs_arg_len(other : dict):
    funcs_arg_len = other


registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]


def getRegister(arg : str , parameters : list):
    assert arg in parameters
    index = parameters.index(arg)
    # print(parameters)
    if index < len(registers):    return registers[index]

def asm_expression(ast, parameters = None, parameters_types = None):

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
            {asm_expression(ast.children[2], parameters)}
            push rax
            {asm_expression(ast.children[0], parameters)}
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
    # print(n)
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