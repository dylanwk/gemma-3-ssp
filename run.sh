#!/bin/bash
# Wrapper script for the TA to easily run the pipeline

# Check if the binary exists
if [ ! -f "./dist/run_pipeline" ]; then
    echo "Error: The compiled binary does not exist. Please compile it first using 'pyinstaller run_pipeline.spec'"
    exit 1
fi

# Run the binary with whatever arguments the TA passes in
./dist/run_pipeline "$@"
