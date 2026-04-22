import argparse
import os
from src.executor import determine_controls, execute_kubescape, generate_csv

def main():
    parser = argparse.ArgumentParser(description="Run Task 3 Executor.")
    parser.add_argument("--names-txt", required=True, help="Path to Task 2 names text file.")
    parser.add_argument("--reqs-txt", required=True, help="Path to Task 2 requirements text file.")
    parser.add_argument("--zip", required=True, help="Path to project-yamls.zip")
    parser.add_argument("--outdir", default="outputs", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    
    base_name = os.path.basename(args.names_txt).replace('diff_names_', '').replace('.txt', '')
    
    controls_txt = os.path.join(args.outdir, f"controls_{base_name}.txt")
    output_csv = os.path.join(args.outdir, f"scan_results_{base_name}.csv")
    
    print(f"Determining controls for {base_name}...")
    determine_controls(args.names_txt, args.reqs_txt, controls_txt)
    
    print(f"Executing Kubescape for {base_name}...")
    df = execute_kubescape(controls_txt, args.zip)
    
    print(f"Generating CSV {output_csv}...")
    generate_csv(df, output_csv)
    
    print(f"Task 3 complete for {base_name}.")

if __name__ == "__main__":
    main()
