main(){
    

    // teste tableaux et pt

    // int[3][4][5] t;
    // a = t[0][0][0];
    // int*** t;
    // a = *(*(*(t+0)+0)+0);
    // t[5+t[9]] = 2;
    // (t[3]) = 6;
    // *(t + 3) = 6;

    int a;
    a = 4;


    int* b;
    b = &a;
    int** c;
    c = &b;

    *(*(c+5-5)+(2*a) - (2*a)) = 5;

    print(int, **c);

    
    

    
    return 0;
}

