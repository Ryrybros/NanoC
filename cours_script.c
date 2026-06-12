

main(){
    int* T;
    int* T2;
    int* R;
    int s;
    s = 5;
    T = malloc(s*8);
    T2 = malloc(s*8);
    int s2;
    s2 = 2*s*8;

    R = malloc(s2);
    standard(T, s, 10);
    standard(T2, s, 0);
    concat(T, s, T2, s, R );

    mergeSort(R, 0, s*2 - 1);

    s2 = 2*s;
    print(str,"Final : ");
    print_tab(R,s2);


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
void standard(int* T, int size, int offset){
    int i;
    i = 0;
    while(i < size){
        *(T + (i*8)) = i + offset;
        i = i + 1;
    }

    
    return 0;
}

int* concat(int* A,int size_A,  int* B, int size_B, int* res){
    int i;
    i = 0;
    while(i < size_A){
        *(res + (i*8)) = *(A + (8*i));
        i = i + 1;
    }
    while(i < (size_A + size_B)){
        *(res + (8*i)) = *(B + (8*(i - size_A)));
        i = i +1;
    }
    return res;
}



void merge(int* arr, int left, int mid, int right) {
    
    print(int, right);
    print(str, " ; ");

    int i;
    int j;
    int k;
    int n1;
    int n2;
    n1 = mid - left + 1;
    n2 = right - mid;

    
    int* leftArr;
    int* rightArr;
    leftArr = malloc(n1*8);
    rightArr = malloc(n2*8);

    
    i = 0;
    j = 0;
    while (i < n1){
        *(leftArr + (8*i)) = *(arr + ((left + (i))*8));
        i = i +1;
    }
    while(j < n2){  
        *(rightArr + (j*8)) = *(arr + (8*(mid + 1 + j)) );
        j = j +1;
    }
        

    
    i = 0;
    j = 0;
    k = left;
    while ( (i < n1) && (j < n2) ) {
            if (*(leftArr + (i*8)) <= *(rightArr + (j*8))) {
                *(arr + (k*8)) = *(leftArr + (i*8));
                i = i +1;
            }
            else {
                *(arr + (k*8)) = *(rightArr + (j*8));
                j= j+1;
            }
            k= k+1;
        
    }
    
    // print(int, n2);
    // print(str, " at merge   ");
    
    while (i < n1) {
        *(arr + (k*8)) = *(leftArr + (i*8));
        i = i +1;
        k= k+1;
    }

    
    while (j < n2) {
        *(arr + (k*8)) = *(rightArr + (j*8));
        j=j+1;
        k=k+1;
    }
    return 0;
}

void mergeSort(int* arr, int left, int right) {
    int mid; 
    // print(int, right);
    // print(str, " ; ");
    
    // print(str, "    ");

    

    if (left < right) {

        mid = left + ((right - left) / 2);

        // print(str, "    ");
        // print(int, mid);
        // print(str, "  and  ");
    
        
        
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        
        print(int, right);
        print(str, "  and  ");

        merge(arr, left, mid, right);
    }else{
        pass;
    }
    return 0;
}

