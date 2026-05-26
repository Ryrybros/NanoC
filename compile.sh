#! bash compile.sh to execute
python3 parser_script.py &&

if nasm -f elf64 -o tuto_assembly/test.o tuto_assembly/test.asm ; then
    echo "Assembled successfully."
else
    echo "Error during assembly!"
    exit 1
fi

gcc -no-pie tuto_assembly/test.o -o tuto_assembly/test.exe

./tuto_assembly/test.exe "$@"
