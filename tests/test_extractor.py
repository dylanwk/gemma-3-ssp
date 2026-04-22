import pytest
import os
import yaml
from src.extractor import (
    load_and_validate_pdfs,
    create_zero_shot_prompt,
    create_few_shot_prompt,
    create_cot_prompt,
    extract_kdes_with_llm,
    log_llm_outputs,
)

from reportlab.pdfgen import canvas


@pytest.fixture
def dummy_pdfs(tmp_path):
    """Fixture to create dummy PDF files for testing."""
    pdf1_path = os.path.join(tmp_path, "cis-r1.pdf")
    pdf2_path = os.path.join(tmp_path, "cis-r2.pdf")

    # Create simple PDFs using reportlab
    c1 = canvas.Canvas(pdf1_path)
    c1.drawString(100, 750, "Authentication requirements for accessing the system.")
    c1.save()

    c2 = canvas.Canvas(pdf2_path)
    c2.drawString(100, 750, "Log management and retention policies.")
    c2.save()

    return pdf1_path, pdf2_path


def test_load_and_validate_pdfs(dummy_pdfs):
    pdf1, pdf2 = dummy_pdfs
    output = load_and_validate_pdfs(pdf1, pdf2)

    assert "cis-r1.pdf" in output
    assert "cis-r2.pdf" in output
    assert "Authentication requirements" in output["cis-r1.pdf"]

    # Test invalid file extension
    test_txt_path = os.path.join(os.path.dirname(pdf1), "test.txt")
    open(test_txt_path, "w").close()
    with pytest.raises(ValueError):
        load_and_validate_pdfs(test_txt_path, pdf2)


def test_create_zero_shot_prompt():
    text = "Sample text for zero shot."
    prompt = create_zero_shot_prompt(text)
    assert "strictly as a YAML dictionary" in prompt
    assert text in prompt


def test_create_few_shot_prompt():
    text = "Sample text for few shot."
    prompt = create_few_shot_prompt(text)
    assert "Example format:" in prompt
    assert text in prompt


def test_create_cot_prompt():
    text = "Sample text for chain of thought."
    prompt = create_cot_prompt(text)
    assert "Let's think step by step" in prompt
    assert text in prompt


def test_extract_kdes_with_llm(tmp_path):
    # Mock LLM pipeline
    def mock_pipeline(*args, **kwargs):
        # Mocks HuggingFace pipeline response
        out_yaml = """
element1:
  name: "Logging"
  requirements:
    - "Centralized logging server."
"""
        return [{"generated_text": out_yaml}]

    doc_name = "test_doc.pdf"
    prompt = "dummy prompt"

    output_dir = os.path.join(tmp_path, "outputs")
    result = extract_kdes_with_llm(
        prompt, doc_name, mock_pipeline, output_dir=output_dir
    )

    assert "element1" in result
    assert result["element1"]["name"] == "Logging"

    # Check if yaml file was created
    yaml_file = os.path.join(output_dir, "test_doc-kdes.yaml")
    assert os.path.exists(yaml_file)
    with open(yaml_file, "r") as f:
        saved_data = yaml.safe_load(f)
        assert saved_data["element1"]["name"] == "Logging"


def test_log_llm_outputs(tmp_path):
    log_file = os.path.join(tmp_path, "llm_outputs.txt")
    entries = [
        {
            "llm_name": "Gemma-3-1B",
            "prompt_used": "PROMPT CONTENT",
            "prompt_type": "Zero Shot",
            "llm_output": "OUTPUT CONTENT",
        }
    ]

    log_llm_outputs(entries, output_filepath=log_file)

    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        content = f.read()
        assert "*LLM Name*\nGemma-3-1B" in content
        assert "*Prompt Used*\nPROMPT CONTENT" in content
        assert "*Prompt Type*\nZero Shot" in content
