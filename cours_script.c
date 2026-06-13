
main(){
    int[10] T;

    fill(T);
    

    print_tab(T);

    return 0; 
}

void fill(int[10] t){
    int n;
    n = len(t);
    int i;

    while( i < n){
        t[i] = i*i + 10;
        i = i + 1;
    }
    return 0;
}

void print_tab(int[10] T){
    int i;
    int size ;
    size = len(T);

    i = 0;
    while(i < size){
        print(int, T[i]);
        print(str, " , ");
        i = i +1;
    }
    return 0;
}