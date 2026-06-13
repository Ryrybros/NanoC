
main(){
    int c;
    

    c = hello(-10) + hallo(2);
    
    print(int,c);
    
    return 0; 
}


int hello(int x){
    int a;
    a = 10 + x;
    x = a +20;
    a = a*x;
    if (a < 10){
    return a;
    }else{
        pass;
    }
}

int hallo(int x){
    return x*x;
}