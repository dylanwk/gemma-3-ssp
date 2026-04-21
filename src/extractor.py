import os
import yaml
from pypdf import PdfReader

def load_and_validate_pdfs(doc1_path: str, doc2_path: str) -> dict:
    """
    Validates the input documents and extracts text from them.
    Ensures that documents exist and are PDFs.
    """
    docs = [doc1_path, doc2_path]
    extracted_data = {}
    
    for doc_path in docs:
        if not os.path.exists(doc_path):
            raise FileNotFoundError(f"Document not found: {doc_path}")
        if not doc_path.lower().endswith('.pdf'):
            raise ValueError(f"Document must be a PDF file: {doc_path}")
        
        try:
            reader = PdfReader(doc_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            extracted_data[os.path.basename(doc_path)] = text.strip()
        except Exception as e:
            raise IOError(f"Error reading PDF {doc_path}: {e}")
            
    return extracted_data

def create_zero_shot_prompt(text: str) -> str:
    """
    Constructs a zero-shot prompt to identify key data elements (KDEs).
    """
    return f"""Identify the key data elements (KDEs) and their specific requirements from the following text.
Do not provide any explanations. Return the result strictly as a YAML dictionary where each KDE has a 'name' and a list of 'requirements'.

Text:
{text}
"""

def create_few_shot_prompt(text: str) -> str:
    """
    Constructs a few-shot prompt to identify key data elements (KDEs) providing an example.
    """
    return f"""Identify the key data elements (KDEs) and their specific requirements from the following text.
Return the result strictly as a YAML dictionary.

Example format:
element1:
  name: "User Password"
  requirements:
    - "Must be at least 8 characters long."
    - "Must contain a special character."

Text:
{text}
"""

def create_cot_prompt(text: str) -> str:
    """
    Constructs a chain-of-thought prompt to identify key data elements (KDEs).
    """
    return f"""Identify the key data elements (KDEs) and their specific requirements from the following text.
Let's think step by step:
1. First, read through the text and identify the main data entities being discussed (e.g., passwords, logs, user data).
2. Then, for each entity, extract the corresponding security requirements or rules mentioned in the document.
3. Finally, format the output strictly as a YAML dictionary where each KDE has a 'name' and a list of 'requirements'.

Text:
{text}
"""

def extract_kdes_with_llm(prompt: str, doc_name: str, llm_pipeline, output_dir: str = "outputs") -> dict:
    """
    Uses the LLM pipeline to identify KDEs based on the prompt,
    saves the output as a YAML file, and returns the nested dictionary.
    """
    # Assuming llm_pipeline is a Hugging Face pipeline
    messages = [
        {"role": "user", "content": prompt},
    ]
    
    outputs = llm_pipeline(messages, max_new_tokens=1024, return_full_text=False)
    llm_response = outputs[0]["generated_text"].strip()
    
    # Try to parse the output as YAML (removing common markdown code blocks)
    clean_yaml = llm_response.replace('```yaml', '').replace('```', '').strip()
    
    try:
        parsed_data = yaml.safe_load(clean_yaml)
        if not isinstance(parsed_data, dict):
            parsed_data = {"raw_output": clean_yaml}
    except Exception as e:
        parsed_data = {"error": str(e), "raw_output": clean_yaml}

    # Save to a YAML file, including the document name
    os.makedirs(output_dir, exist_ok=True)
    yaml_filename = os.path.join(output_dir, f"{os.path.splitext(doc_name)[0]}-kdes.yaml")
    
    with open(yaml_filename, 'w') as f:
        yaml.dump(parsed_data, f, default_flow_style=False, sort_keys=False)
        
    return parsed_data

def log_llm_outputs(log_entries: list, output_filepath: str = "outputs/llm_outputs.txt"):
    """
    Collects outputs of all LLMs and dumps them into a formatted TEXT file.
    log_entries should be a list of dictionaries with keys:
    'llm_name', 'prompt_used', 'prompt_type', 'llm_output'
    """
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, 'w') as f:
        for entry in log_entries:
            f.write(f"*LLM Name*\n{entry.get('llm_name', 'Unknown')}\n")
            f.write(f"*Prompt Used*\n{entry.get('prompt_used', '')}\n")
            f.write(f"*Prompt Type*\n{entry.get('prompt_type', '')}\n")
            f.write(f"*LLM Output*\n{entry.get('llm_output', '')}\n")
            f.write("-" * 40 + "\n")
