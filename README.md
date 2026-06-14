# NanoC
This is a compilation project where a group of 3 students create their own language, the language is parsed using LARK and compiled using assembly.

To compile using variables of the main function, for instance main(arg1, arg2, arg3, ...) run "bash compile.sh arg1 arg2 arg3 ...". The arguments of main are necessary int.

Opération interdite : 

&expression, que &NAME

int[] *** : adressage de tableau


python parser : 
verif que on prend pas l'adresse d'un type tableau
verif meme type dans un tableau


en creant un pointer p, on a p[7] donc aucune secu memoire

Ne marche pas car on ne prend pas l'adresse des tableaux statiques    g = *i[8] <=> g = (*i)[8]; mais quand est il des dynamiques ? on doit faire une étape intermédiaire
pour for : var muette i a initialiser dans data/scope des fcts, puis transfo for en while

Supprimer ttes les branches sauf main

Victor : fct gene de deref arirthm des pts

POUR CLAUDE : 

fct tabToPt : prend l'arbre ast d'un tableau et tente de le convertir en l'arbre ast d'un pt, c'est encore experimentale donc je sais pas du tout si ca marche dans tout les cas, en tout cas ça marche sur l'exemple qu'il y a dans cours_script et c'est un bon début montrant que c'est possible

fct asm_expression : grace a tabToPt, renvoie eltab_read à dereferencing

le malloc ainsi que l'arithmetique des pts marchent, dans "tests", tu trouveras des exemples très proche des tableaux dynamiques

Pour terminer, j'ai rajouter deux fonctions : asm_lexpression qui calcule des expressions qui vont être assignées à gauche et asm_command_asign qui a partir d'une left expression calculée avec asm_lexpression et une right expression calculée avec asm_expression, assigne les deux selon le type d'assignement


**Arithmetic:**
The operator priority is not recognized: a + b*c = (a + b)*c, use parenthesis to be explicit : a + (b*c)
The language handles + , -, *, /
Arithmetic is allowed on function calls : a = a + f(b)


**Functions:**

Functions are declared using the classic typed syntaxe !! main is not typed.

Function arguments should have typed arguments,

The returned value of a function should match the type of the function, besides, a return is required (if there are if_else : it is required to either have the return at the end of in each branch of if and else)

If the function is of type void, a return is still required to declare the end of the function (you can return 0) the returned value is not actually allowed to be used because the type is void (block by the compiler).


Functions can be recursive.
They can return int , tables and pointers of all type

Example :
        

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






**TYPES**
The types of the language are int , int[1] , int[2] ,int*, int** ,... int[n] , int**....*
It is not possible to do binary operations between 2 different types.
except for :
Pointer arithmetic is allowed : example : *(p + 8) returns the value at p with an offset of 8 (size of an int)
Example :
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



**Pointers:**
























**Tables:**


