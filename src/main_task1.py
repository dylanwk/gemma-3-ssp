import os
import argparse
import torch
from transformers import pipeline
from src.extractor import (
    load_and_validate_pdfs,
    sample_pages,
    create_zero_shot_prompt,
    create_few_shot_prompt,
    create_cot_prompt,
    extract_kdes_with_llm,
    log_llm_outputs,
)


def main():
    parser = argparse.ArgumentParser(
        description="Run Task 1 Extractor on two PDF files."
    )
    parser.add_argument("--doc1", required=True, help="Path to the first PDF document.")
    parser.add_argument(
        "--doc2", required=True, help="Path to the second PDF document."
    )
    args = parser.parse_args()

    # Load and validate PDFs
    print(f"Loading documents: {args.doc1} and {args.doc2}")
    doc_data = load_and_validate_pdfs(args.doc1, args.doc2)

    # Store all prompts
    all_prompts = {"zero-shot": [], "few-shot": [], "chain-of-thought": []}
    log_data = []

    print("Initializing Gemma-3-1B model (this may take a moment)...")

    # Use Apple Silicon GPU (MPS) if available, otherwise fallback to CPU
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")

    llm_pipeline = pipeline(
        "text-generation",
        model="google/gemma-3-1b-it",
        device=device,
        torch_dtype=torch.float16 if device == "mps" else torch.bfloat16,
    )

    # Process each document
    for doc_name, pages in doc_data.items():
        print(f"\nProcessing {doc_name}...")

        # Sample pages to process (max 5)
        sampled = sample_pages(pages, max_pages=5)
        print(f"Sampled {len(sampled)} pages for {doc_name}.")

        # Generate prompts for all sampled pages
        zero_shot_prompts = [create_zero_shot_prompt(page) for page in sampled]
        few_shot_prompts = [create_few_shot_prompt(page) for page in sampled]
        cot_prompts = [create_cot_prompt(page) for page in sampled]

        all_prompts["zero-shot"].extend(zero_shot_prompts)
        all_prompts["few-shot"].extend(few_shot_prompts)
        all_prompts["chain-of-thought"].extend(cot_prompts)

        # Process all 3 prompt types to satisfy the assignment requirement
        print(f"Extracting KDEs for {doc_name} using all 3 prompts...")

        for p_type, prompts_list in [
            ("Zero Shot", zero_shot_prompts),
            ("Few Shot", few_shot_prompts),
            ("Chain of Thought", cot_prompts),
        ]:
            # Temporarily alter doc name so it caches all 3 prompt results uniquely
            doc_name_unique = f"{doc_name}_{p_type.replace(' ', '_')}"
            yaml_output = extract_kdes_with_llm(
                prompts_list, doc_name_unique, llm_pipeline, output_dir="outputs"
            )

            # Log the LLM run for each prompt type
            log_data.append(
                {
                    "llm_name": "google/gemma-3-1b-it",
                    "prompt_used": "\n\n---\n\n".join(prompts_list),
                    "prompt_type": p_type,
                    "llm_output": str(yaml_output),
                }
            )

        # Create the final primary YAML used by downstream tasks (Task 2)
        # We will default to Chain Of Thought as the primary
        _ = extract_kdes_with_llm(
            cot_prompts, doc_name, llm_pipeline, output_dir="outputs"
        )

    # Save PROMPT.md (Appending so all 9 inputs are collected)
    print("\nSaving prompts to PROMPT.md...")
    with open("outputs/PROMPT.md", "a") as f:
        for p_type, prompts in all_prompts.items():
            f.write(f"## {p_type}\n\n")
            for prompt in prompts:
                f.write(f"```text\n{prompt}\n```\n\n")

    # Save logs
    print("Saving text logs to llm_outputs.txt...")
    log_llm_outputs(log_data, output_filepath="outputs/llm_outputs.txt")

    print("\nTask 1 processing complete. Check the 'outputs' directory for results.")


if __name__ == "__main__":
    main()
