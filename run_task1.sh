#!/bin/bash

# Ensure we're in the virtual environment
source .venv/bin/activate

echo "Cleaning previous outputs..."
rm -f outputs/*.yaml outputs/*.txt outputs/*.md

echo "Running all 9 input combinations for Task 1..."

# Input 1: cis-r1.pdf and cis-r1.pdf
python3 main_task1.py --doc1 data/cis-r1.pdf --doc2 data/cis-r1.pdf

# Input 2: cis-r1.pdf and cis-r2.pdf
python3 main_task1.py --doc1 data/cis-r1.pdf --doc2 data/cis-r2.pdf

# Input 3: cis-r1.pdf and cis-r3.pdf
python3 main_task1.py --doc1 data/cis-r1.pdf --doc2 data/cis-r3.pdf

# Input 4: cis-r1.pdf and cis-r4.pdf
python3 main_task1.py --doc1 data/cis-r1.pdf --doc2 data/cis-r4.pdf

# Input 5: cis-r2.pdf and cis-r2.pdf
python3 main_task1.py --doc1 data/cis-r2.pdf --doc2 data/cis-r2.pdf

# Input 6: cis-r2.pdf and cis-r3.pdf
python3 main_task1.py --doc1 data/cis-r2.pdf --doc2 data/cis-r3.pdf

# Input 7: cis-r2.pdf and cis-r4.pdf
python3 main_task1.py --doc1 data/cis-r2.pdf --doc2 data/cis-r4.pdf

# Input 8: cis-r3.pdf and cis-r3.pdf
python3 main_task1.py --doc1 data/cis-r3.pdf --doc2 data/cis-r3.pdf

# Input 9: cis-r3.pdf and cis-r4.pdf
python3 main_task1.py --doc1 data/cis-r3.pdf --doc2 data/cis-r4.pdf

echo "Completed processing all 9 inputs!"
