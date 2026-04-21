import os
import argparse
from src.extractor import (
    load_and_validate_pdfs,
    create_zero_shot_prompt,
    create_few_shot_prompt,
    create_cot_prompt,
    extract_kdes_with_llm,
    log_llm_outputs
)

# Replace with the actual model initialization logic if testing locally
# e.g., from transformers import pipeline
# pipeline = pipeline("text-generation", model="google/gemma-3-1b-it")
def mock_llm_pipeline(messages, **kwargs):
    # This is a mock pipeline for testing without the full LLM weights.
    prompt_text = messages[0]["content"]
    yaml_mock = """
element1:
  name: "Mock Data Element"
  requirements:
    - "Mock requirement 1"
    - "Mock requirement 2"
"""
    return [{"generated_text": yaml_mock}]

def main():
    parser = argparse.ArgumentParser(description="Run Task 1 Extractor on two PDF files.")
    parser.add_argument("--doc1", required=True, help="Path to the first PDF document.")
    parser.add_argument("--doc2", required=True, help="Path to the second PDF document.")
    args = parser.parse_args()

    # Load and validate PDFs
    print(f"Loading documents: {args.doc1} and {args.doc2}")
    doc_data = load_and_validate_pdfs(args.doc1, args.doc2)
    
    # Store all prompts
    all_prompts = {"zero-shot": [], "few-shot": [], "chain-of-thought": []}
    log_data = []

    # Process each document
    for doc_name, text in doc_data.items():
        print(f"\nProcessing {doc_name}...")
        
        # 1. Zero Shot
        zero_shot_prompt = create_zero_shot_prompt(text)
        all_prompts["zero-shot"].append(zero_shot_prompt)
        
        # 2. Few Shot
        few_shot_prompt = create_few_shot_prompt(text)
        all_prompts["few-shot"].append(few_shot_prompt)
        
        # 3. Chain of Thought
        cot_prompt = create_cot_prompt(text)
        all_prompts["chain-of-thought"].append(cot_prompt)

        # For execution, we're using the COT prompt as the primary strategy to generate the YAML
        # (Could be modified to use the best performing prompt)
        print(f"Extracting KDEs for {doc_name} using Gemma-3-1B...")
        
        # Note: Swap mock_llm_pipeline with an actual instantiated Hugging Face pipeline
        llm_pipeline = mock_llm_pipeline 
        
        yaml_output = extract_kdes_with_llm(cot_prompt, doc_name, llm_pipeline, output_dir="outputs")
        
        # Log the LLM run
        log_data.append({
            "llm_name": "google/gemma-3-1b-it",
            "prompt_used": cot_prompt,
            "prompt_type": "Chain of Thought",
            "llm_output": str(yaml_output)
        })

    # Save PROMPT.md
    print("\nSaving prompts to PROMPT.md...")
    with open("outputs/PROMPT.md", "w") as f:
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
