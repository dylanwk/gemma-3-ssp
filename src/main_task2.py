import argparse
import os
from src.comparator import compare_names, compare_requirements

def main():
    parser = argparse.ArgumentParser(description="Run Task 2 Comparator on two YAML files.")
    parser.add_argument("--yaml1", required=True, help="Path to the first YAML document.")
    parser.add_argument("--yaml2", required=True, help="Path to the second YAML document.")
    parser.add_argument("--outdir", default="outputs", help="Directory to save output TXT files.")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    
    base1 = os.path.splitext(os.path.basename(args.yaml1))[0]
    base2 = os.path.splitext(os.path.basename(args.yaml2))[0]
    
    names_out = os.path.join(args.outdir, f"diff_names_{base1}_vs_{base2}.txt")
    reqs_out = os.path.join(args.outdir, f"diff_reqs_{base1}_vs_{base2}.txt")
    
    print(f"Comparing names between {base1} and {base2}...")
    compare_names(args.yaml1, args.yaml2, names_out)
    
    print(f"Comparing requirements between {base1} and {base2}...")
    compare_requirements(args.yaml1, args.yaml2, reqs_out)
    
    print(f"Task 2 complete for {base1} and {base2}.")

if __name__ == "__main__":
    main()
