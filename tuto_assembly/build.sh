

#!/bin/bash

# 1. Assemble with NASM
# We check if nasm succeeds before moving to the next step
if nasm -f elf64 -o test.o $1 ; then
    echo "Assembled successfully."
else
    echo "Error during assembly!"
    exit 1
fi

gcc -no-pie test.o -o test.exe

./test.exe


