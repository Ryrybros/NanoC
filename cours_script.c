main(){
    
    int*p;
    int a;
    a = 4;
    p = &a;
    
    print(int, f(p));
    p = g(10);
    print(int, f(p));

    
    return 0;
}

int f(int* p){
    return *p;
}

int g(int a){
    int* p;
    p = &a;
    return p;
}

