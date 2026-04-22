#!/bin/bash

# Ensure we're in the virtual environment
source .venv/bin/activate

echo "Running Task 2 Comparator on Task 1 output pairs..."

# Input 1: cis-r1 and cis-r1
python3 src/main_task2.py --yaml1 outputs/cis-r1-kdes.yaml --yaml2 outputs/cis-r1-kdes.yaml

# Input 2: cis-r1 and cis-r2
python3 src/main_task2.py --yaml1 outputs/cis-r1-kdes.yaml --yaml2 outputs/cis-r2-kdes.yaml

# Input 3: cis-r1 and cis-r3
python3 src/main_task2.py --yaml1 outputs/cis-r1-kdes.yaml --yaml2 outputs/cis-r3-kdes.yaml

# Input 4: cis-r1 and cis-r4
python3 src/main_task2.py --yaml1 outputs/cis-r1-kdes.yaml --yaml2 outputs/cis-r4-kdes.yaml

# Input 5: cis-r2 and cis-r2
python3 src/main_task2.py --yaml1 outputs/cis-r2-kdes.yaml --yaml2 outputs/cis-r2-kdes.yaml

# Input 6: cis-r2 and cis-r3
python3 src/main_task2.py --yaml1 outputs/cis-r2-kdes.yaml --yaml2 outputs/cis-r3-kdes.yaml

# Input 7: cis-r2 and cis-r4
python3 src/main_task2.py --yaml1 outputs/cis-r2-kdes.yaml --yaml2 outputs/cis-r4-kdes.yaml

# Input 8: cis-r3 and cis-r3
python3 src/main_task2.py --yaml1 outputs/cis-r3-kdes.yaml --yaml2 outputs/cis-r3-kdes.yaml

# Input 9: cis-r3 and cis-r4
python3 src/main_task2.py --yaml1 outputs/cis-r3-kdes.yaml --yaml2 outputs/cis-r4-kdes.yaml

echo "Task 2 processing complete! Check outputs/ for txt files."
