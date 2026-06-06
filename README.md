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






