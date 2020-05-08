for f in topo/*; do
    time -o 1.txt -a -f "%E" sudo python3 main.py $f >> 1.txt
done
