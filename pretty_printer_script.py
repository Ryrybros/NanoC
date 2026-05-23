
def pp_expression(ast):
    
    if ast.data in  ( "variable" , "int"  ):
        return ast.children[0].value
    lo = f"{pp_expression(ast.children[0])}"
    op = f"{ast.children[1].value}"
    ro = f"{pp_expression(ast.children[2])}"
    return lo + " " + op + " " + ro


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
