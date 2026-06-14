

main(){
    int n;
    n = 3;

    int* T1;
    int* T2;
    int* T3;
    
    T1 = malloc(n*8);

    shuffled(T1, n,0);
    print_tab(T1,n);

    return 0;
}

void print_tab(int* T, int size){
    
    for(int i = 0; i < size ; i++){
        print(int, T[i]);
        print(str, " , ");
    }
    return 0;
}


void standard(int* T, int size, int offset){
    
    for(int i = 0; i < size ; i++){
        T[i] = i + offset;
        
    }

    
    return 0;
}

void shuffled(int* T, int size, int offset){
    
    for(int i = 0; i < size ; i++){
        T[i] = ( 5-(i + offset))*(i + offset)*( 10-(i + offset)) ;
        
    }

    
    return 0;
}




