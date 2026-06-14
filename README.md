# NanoC
This is a compilation project where a group of 3 students create their own language, the language is parsed using LARK and compiled using assembly.

To compile using variables of the main function, for instance main(arg1, arg2, arg3, ...) run "bash compile.sh arg1 arg2 arg3 ...". The arguments of main are necessary int. The code that will compiled is in cours_script.c.
Warning : if the compilation fails, then compile.sh executes the last assembly code.

This language handles functions (Ryad Gourine), pointers (Victor Gasse) and arrays (Claude Leroy).

Several tests for the different features are proposed in the scripts in tests/scripts and tested in tester.py.

The compiler forbids the user to do many of the unallowed operations. It especially checks the types of the variables and expressions and raise a TypeError when these types are not compatible.



**Arithmetic:**
The operator priority is not recognized: a + b*c = (a + b)*c, use parenthesis to be explicit : a + (b*c)
The language handles + , -, *, /
Arithmetic is allowed on function calls : a = a + f(b)
Arithmetic is not allowed on arrays, but it is allowed on array elements as long as they are of a type that allows arithmetic operations.



**Functions:**
Functions are declared using the classic typed syntaxe !! main is not typed.

Function arguments should have typed arguments.

The returned value of a function should match the type of the function, besides, a return is required (if there are if_else : it is required by the compiler to either have the return at the end or in each branch of if and else).

If the function is of type void, a return is still required to declare the end of the function (you can return 0) the returned value is not actually allowed to be used because the type is void (blocked by the compiler).


Functions can be recursive.
They can return int, arrays and pointers of all type

Example:                
        
        int fib(int n){
            
            if(n < 2){
                return n ;
            }else{
                return fib(n - 2) + fib(n - 1);
            }
        }
        
        main(){
            int c ;
            c = 10;
            c = fib(c);
            
            print(int,c);
            
            return 0; 
        }


**
For a more developped example check merge sort in the test scripts
**        

At each function call, each register used to store function parameters is pushed into the stack and popped to get it back after the function call.
Furthermore, at each call of printf or malloc, every register used by the compiler are pushed and popped. 
For variables, while vairables declared in main are stored in section.data, variables declared in functions are put on the stack and accessed using rbp - offset.
Finally, each function of the compiler has variables_dict and parameters as arguments to keep track of current local variables and function parameters (to allow variables in functions and in main to have the same name).




**TYPES**
The types of the language are int , int[1] , int[2] ,int*, int** ,... int[n] , int**....*, int*[2], ...
Each variable declaration should be done before any assignment.
It is not possible to do binary operations between 2 different types, except for pointers:
Pointer arithmetic is allowed: *(p + 8) returns the value at p with an offset of 8 (size of an int)
Example:
    main(){
        int* T;
        int s;
        s = 5;
        T = malloc(s*8);
        standard(T, s);
        print_tab(T, s);
        return 0;
    }
        
    void print_tab(int* T, int size){
        int i;
        i = 0;
        while(i < size){
            print(int, *(T + (i*8)));
            print(str, " , ");
            i = i +1;
        }
        return 0;
    }
        
    void standard(int* T, int size){
        int i;
        i = 0;
        while(i < size){
            *(T + (i*8)) = i*10;
            i = i + 1;
        }        
        return 0;
    }


asm_compare_types_expression is a reccursive run of the ast tree ensuring that expression respect types.
The types are also checked in asm_command for some commands.




**Pointers:**
Pointers are declared using the syntax: int* p. It is possible to declare pointers of pointers: int*** p. It is not possible to declare a pointer of an array: int[]*.
A pointer can be dereferenced using the syntax: *p. It is also possible to dereference an expression using parentheses: *(expr).
The address of a variable can be obtained using the syntax: &var. It is not possible to get the address of an expression.

Since pointers are considered as dynamic arrays (and vice versa), it is possible to access the value of ptr+(8*i) with ptr[i]. This means that the access to the memory is not secure.

It is possible to allocate memory with the function malloc: malloc(n) allocates a size n in memory.

Example:
    main(){
        int a;
        a = 4;
        int*** b;
        int** c;
        int* d;
        d = &a;
        c = &d;
        b = &c;
        int x;
        x = ***b;
        print(int, x);
        return 0;
    }

The pointers declared in functions (main included) are automatically deallocated at the end of the scope of the function. 


**Arrays:**
There are two types of arrays:
    Static arrays: A static array of size N and type TYPE is declared by writing TYPE[N]. TYPE can be int or a pointer, N is a positive integer and can't be an expression or a variable. An array of arrays is declared with TYPE[N1][N2] for an array of N1 arrays each of size N2.
    An element of an array can be obtained with T[i], and T[i][j] for a multi-sized array.
    The length of a static array T can be obtained with len(T), and appears in its type.
    A static array that has been declared can be assigned directly with an array: T = [1,2,3]. This works with int or variables in the array.
    When used as an argument in a function, the length of an array is fixed by its type, so a function can't use arrays of different types in the same argument.

    Dynamic arrays: A dynamic array is a pointer and is declared as such. A pointer of a pointer is thus a multi-sized array.
    The elements of a dynamic array (and of a pointer) can be obtained in the same way as for a static array.
    The length of a dynamic array is not defined, so any element can be accessed. len is not defined for a dynamic array.
    A dynamic array can't be assigned directly with [1,2,3].

The arrays composing a multi-sized array should be declared before being assigned to the multi-sized array. In particular, it is not possible to access an element T[i][j] before an assignment of the array in T[i].
It is not possible to get the address of an element in an array (&T[i]), it should be done separately: a = T[i]; &a.
To dereference the value of an element of an array, parentheses should be used: *(T[i]).


Example:
    main() {
        int[2][3] t;
        int[3] a;
        t[0] = a;
        a[1] = 5;
        int[3] b;
        b = [1,2,3];
        t[1] = b;
        print(int, t[0][1]);
        for(int i = 0; i < len(t[1]); i++)
        {
            print(int, t[1][i]);
        }
        return 0;
    }


Static arrays are pointers pointing to the first element of this array, the other elements can be accessed by using pointer arithmetic.
An access to the i-th element of a (static or dynamic) array t is converted to an access to the value of the pointer t+(8*i), since 8 is the size of an int.



**For loops:**
The language handles for loops in main and in the functions.
The syntax of this loop is strict, as it was added near the end of the project: for(int var = expr1; var < expr2; var++) {command}
where only var, expr1, expr2 and command can be modified. It thus allows only loops on an increasing integer.
Nested loops are not possible in this language.
var can be called in the scope of the loop (command), but should not be used outside of this scope (the behavior for this possibility was not defined).
Other variables can be declared and used inside of the scope of the loop.

Example:
    main(){
        int[5] t;
        t = [1,2,3,4,5];
        for(int i = 0; i < len(t); i++)
        {
            int k;
            k = t[i]-1;
            print(int, k);
        }
        return 0; 
    }

The counter variable in the loop is stored in the r11 register and not declared with the other variables at the start of the code. It is temporarily considered as a variable in the scope.


