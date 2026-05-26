#! bash compile.sh to execute
python3 parser_script.py

if nasm -f elf64 -o tuto_assembly/test.o tuto_assembly/test.asm ; then
    echo "Assembled successfully."
else
    echo "Error during assembly!"
    exit 1
fi

gcc -no-pie test.o -o test.exe

./test.exe "$@"
