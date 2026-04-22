import pytest
import os
import yaml
from src.comparator import _normalize_kdes, load_yamls, compare_names, compare_requirements

@pytest.fixture
def sample_yamls(tmp_path):
    yaml1_path = os.path.join(tmp_path, "file1.yaml")
    yaml2_path = os.path.join(tmp_path, "file2.yaml")
    
    data1 = {
        "KDE1": {
            "name": "Access Control",
            "requirements": ["Must have MFA"]
        },
        "KDE2": [
            {"name": "Logging"},
            {"requirements": ["Keep for 30 days"]}
        ]
    }
    
    data2 = {
        "KDE1": {
            "name": "Access Control",
            "requirements": ["Must have MFA", "Must have complex passwords"]
        },
        "KDE3": {
            "name": "Encryption",
            "requirements": ["AES-256"]
        }
    }
    
    with open(yaml1_path, 'w') as f:
        yaml.dump(data1, f)
        
    with open(yaml2_path, 'w') as f:
        yaml.dump(data2, f)
        
    return yaml1_path, yaml2_path

def test_normalize_kdes():
    raw = {
        "item1": {"name": "Test1", "requirements": ["r1"]},
        "item2": [{"Name": "Test2"}, {"Requirements": ["r2"]}]
    }
    norm = _normalize_kdes(raw)
    assert "test1" in norm
    assert "test2" in norm
    assert norm["test1"]["requirements"] == ["r1"]
    assert norm["test2"]["requirements"] == ["r2"]

def test_load_yamls(sample_yamls):
    y1, y2 = sample_yamls
    n1, n2 = load_yamls(y1, y2)
    assert "access control" in n1
    assert "logging" in n1
    assert "encryption" in n2

def test_compare_names(sample_yamls, tmp_path):
    y1, y2 = sample_yamls
    out_path = os.path.join(tmp_path, "names.txt")
    
    compare_names(y1, y2, out_path)
    
    with open(out_path, 'r') as f:
        content = f.read()
    
    assert "Logging" in content
    assert "Encryption" in content
    assert "Access Control" not in content
    
def test_compare_names_no_diff(tmp_path):
    y1 = os.path.join(tmp_path, "empty1.yaml")
    with open(y1, 'w') as f:
        yaml.dump({"KDE1": {"name": "Same", "requirements": []}}, f)
        
    out_path = os.path.join(tmp_path, "names_same.txt")
    compare_names(y1, y1, out_path)
    
    with open(out_path, 'r') as f:
        content = f.read().strip()
    assert content == "NO DIFFERENCES IN REGARDS TO ELEMENT NAMES"

def test_compare_requirements(sample_yamls, tmp_path):
    y1, y2 = sample_yamls
    out_path = os.path.join(tmp_path, "reqs.txt")
    
    compare_requirements(y1, y2, out_path)
    
    with open(out_path, 'r') as f:
        lines = f.read().splitlines()
        
    # Access Control,ABSENT-IN-file1.yaml,PRESENT-IN-file2.yaml,Must have complex passwords
    assert any("Access Control" in l and "Must have complex passwords" in l for l in lines)
    # Logging,ABSENT-IN-file2.yaml,PRESENT-IN-file1.yaml,NA
    assert any("Logging" in l and "NA" in l and "PRESENT-IN-file1.yaml" in l for l in lines)
    
def test_compare_requirements_no_diff(tmp_path):
    y1 = os.path.join(tmp_path, "empty1.yaml")
    with open(y1, 'w') as f:
        yaml.dump({"KDE1": {"name": "Same", "requirements": ["r1"]}}, f)
        
    out_path = os.path.join(tmp_path, "reqs_same.txt")
    compare_requirements(y1, y1, out_path)
    
    with open(out_path, 'r') as f:
        content = f.read().strip()
    assert content == "NO DIFFERENCES IN REGARDS TO ELEMENT REQUIREMENTS"
