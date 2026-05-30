import os
import lark


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



def pp_args(ast):
    if ast.data == "var":
        variable = ast.children[0].value 
        return variable
    if ast.data == "arglist":

        arglist = ast.children
        res =  f"{arglist[0].children[0].value} {arglist[0].children[1].value}"
        if len(ast.children) > 1 :
            for i in range(1 ,len(ast.children)):
                res += f" , {ast.children[i].children[0].value} {ast.children[i].children[1].value}"
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

    if ast.data == 'declaration' :
        val = ""
        if len(ast.children) > 1 : val = f" {ast.children[1]}"
        return f"""{ast.children[0].value} {val}  """

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


