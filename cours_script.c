main(){
    

    // teste tableaux et pt
    int a;
    // int[3][4][5] t;
    int*** t;
    t = malloc(8);
    *t = malloc(8);

    **t = malloc(8);

    ***t = 7;

    a = t[0][0][0];
    print(int, a);
    // int*** t;
    // a = *(*(*(t+0)+0)+0);
    // t[5+t[9]] = 2;
    // (t[3]) = 6;
    // *(t + 3) = 6;


    
    

    
    return 0;
}

