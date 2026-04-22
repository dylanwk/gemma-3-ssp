import argparse
import os
import sys

# Import the main functions from the task modules
import src.main_task1 as main_task1
import src.main_task2 as main_task2
import src.main_task3 as main_task3

def run_task1(doc1, doc2):
    # Mock sys.argv to pass arguments to the imported main functions
    sys.argv = ["main_task1.py", "--doc1", doc1, "--doc2", doc2]
    main_task1.main()

def run_task2(yaml1, yaml2):
    sys.argv = ["main_task2.py", "--yaml1", yaml1, "--yaml2", yaml2]
    main_task2.main()
    
def run_task3(names_txt, reqs_txt, zip_path):
    sys.argv = ["main_task3.py", "--names-txt", names_txt, "--reqs-txt", reqs_txt, "--zip", zip_path]
    main_task3.main()

def main():
    parser = argparse.ArgumentParser(description="Run full security requirements pipeline (Tasks 1-3).")
    parser.add_argument("--doc1", required=True, help="Path to first PDF.")
    parser.add_argument("--doc2", required=True, help="Path to second PDF.")
    parser.add_argument("--zip", default="project-yamls.zip", help="Path to Kubescape target ZIP.")
    
    # If no args provided, we could just display help or run a default, but we'll let argparse handle it
    args, unknown = parser.parse_known_args()
    
    print("="*40)
    print(f"RUNNING PIPELINE FOR: {args.doc1} and {args.doc2}")
    print("="*40)
    
    print("\n[PHASE 1] Extractor")
    run_task1(args.doc1, args.doc2)
    
    base1 = os.path.basename(args.doc1).replace('.pdf', '')
    base2 = os.path.basename(args.doc2).replace('.pdf', '')
    yaml1 = f"outputs/{base1}-kdes.yaml"
    yaml2 = f"outputs/{base2}-kdes.yaml"
    
    print("\n[PHASE 2] Comparator")
    run_task2(yaml1, yaml2)
    
    names_txt = f"outputs/diff_names_{base1}-kdes_vs_{base2}-kdes.txt"
    reqs_txt = f"outputs/diff_reqs_{base1}-kdes_vs_{base2}-kdes.txt"
    
    print("\n[PHASE 3] Executor")
    run_task3(names_txt, reqs_txt, args.zip)
    
    print("\n[PIPELINE COMPLETE]")

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()
