# Matrix multiplication with Strassen algorithm

Uses NumPy matrices stored in .npy files. Performs multiplication 
with Strassen algorithm (single- or multi-threaded). Default is single-threaded Strassen implementation.

# Usage

Generate matrix:

    ./main.py -g N M [-o FILE]
    
Print matrix:

    ./main.py FILE

Multiply matrices:

    ./main.py FILE1 FILE2 [-o FILE3] [-n/--naive] [-m/--multi] [-t/--timing]
        -n, --naive:   use trivial algorithm
        -m, --multi:   use multithreading (for Strassen)
        -t, --timing:  only measure timing, do not store result
