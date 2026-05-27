from parser_script import *
import sys
arguments = sys.argv[1:]
if len(arguments) == 0 : run()

else:
    print(f"running : {''.join(arguments)} ...") 
    with open(''.join(arguments),"r") as f:
        run(f.read()) 