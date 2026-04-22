#!/bin/bash

# Ensure we're in the virtual environment
source .venv/bin/activate

echo "Running Task 3 Executor on Task 2 outputs..."

ZIP_FILE="project-yamls.zip"

for f in outputs/diff_names_*.txt; do
    # Extract the base pair string, e.g. cis-r1-kdes_vs_cis-r2-kdes
    BASE=$(basename "$f" | sed 's/diff_names_//' | sed 's/.txt//')
    
    REQS_FILE="outputs/diff_reqs_${BASE}.txt"
    
    if [ -f "$REQS_FILE" ]; then
        python3 src/main_task3.py \
            --names-txt "$f" \
            --reqs-txt "$REQS_FILE" \
            --zip "$ZIP_FILE"
    fi
done

echo "Task 3 processing complete! Check outputs/ for csv files."
