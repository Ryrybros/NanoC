import os
import lark




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
    


if __name__ == "__main__":

    path = "pretty_script"
    grammar_path = "cours_grammar"
    with open(path) as f:
        script = f.read()
    with open(grammar_path) as f:
        grammar = f.read()

    gram = f''' {grammar} '''

    l = lark.Lark(gram)
    t = l.parse(script, start = "start")
    print(t.pretty())
    # print(pp_command(t.children[0]))


