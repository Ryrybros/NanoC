main(){
    int a;
    a = 4;
    int*** b;
    int** c;
    int* d;
    int**** e;
    int**** t;
    d = &a;
    c = &d;
    b = &c;
    e = &b;
    int x;
    // x = x + d;
    // x = ***(*(e+a*2 + 8 - 2*a - 8)+9*a - 9*a);
    x = ****e;
    
    
    print(int, x);
    
    return 0;
}


